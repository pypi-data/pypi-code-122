# -*- coding : utf-8 -*-
# @Time   : 2021/10/1 16:15
# @Author : goodli
# @File   : classify_trainer.py
# @Project: Valley 山谷

import os
import random
import logging
import time
import weakref
import numpy as np

import torch
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.nn.functional as F

import torch.distributed as dist
from torch.utils.data.distributed import DistributedSampler
import argparse

from torch.utils.tensorboard import SummaryWriter

from valley.utils import Logger
from valley.utils import comm
from valley.utils.events import CommonMetricPrinter, JSONWriter, TensorboardXWriter, get_event_storage
from valley.utils.file_io import PathManager

import valley.utils.plugin

from valley.utils.plugin  import reg_plugin, PluginType
import valley.utils.plugin as plugin
from valley.config import configurable

from valley.model import build_model
from valley.data import build_train_dataloader, build_test_dataloader

from valley.data import DataPhase, DataType
from valley.solver import build_lr_scheduler, build_optimizer


from valley.evaluator import build_evaluator
from valley.engine.train_loop import TrainerBase
from valley.checkpoint import VCheckpointer

from valley.engine import hooks
from typing import Dict, Optional

from .train_loop import AMPTrainer, SimpleTrainer, TrainerBase
from collections import OrderedDict
from valley.evaluator import DatasetEvaluator, inference_on_dataset
from valley.evaluator import print_csv_format

def print_model_param(model):
    for name, parameters in model.named_parameters():
        print(name, ':',  parameters)
        break


def default_writers(output_dir: str, iters_per_epoch: int, max_iter: Optional[int] = None):
    """
    Build a list of :class:`EventWriter` to be used.
    It now consists of a :class:`CommonMetricPrinter`,
    :class:`TensorboardXWriter` and :class:`JSONWriter`.

    Args:
        output_dir: directory to store JSON metrics and tensorboard events
        iters_per_epoch: iters per epoch
        max_iter: the total number of iterations

    Returns:
        list[EventWriter]: a list of :class:`EventWriter` objects.
    """
    return [
        # It may not always print what you want to see, since it prints "common" metrics only.
        CommonMetricPrinter(iters_per_epoch, max_iter),
        #JSONWriter(os.path.join(output_dir, "metrics.json")),
        #TensorboardXWriter(output_dir),
    ]


def create_ddp_model(model, *, fp16_compression=False, **kwargs):
    """
    Create a DistributedDataParallel model if there are >1 processes.
    Args:
        model: a torch.nn.Module
        fp16_compression: add fp16 compression hooks to the ddp object.
            See more at https://pytorch.org/docs/stable/ddp_comm_hooks.html#torch.distributed.algorithms.ddp_comm_hooks.default_hooks.fp16_compress_hook
        kwargs: other arguments of :module:`torch.nn.parallel.DistributedDataParallel`.
    """  # noqa
    if comm.get_world_size() == 1:
        return model
    if "device_ids" not in kwargs:
        kwargs["device_ids"] = [comm.get_local_rank()]
    
    ddp = DDP(model, **kwargs)
    if fp16_compression:
        from torch.distributed.algorithms.ddp_comm_hooks import default as comm_hooks

        ddp.register_comm_hook(state=None, hook=comm_hooks.fp16_compress_hook)

    return ddp

def default_argument_parser(epilog=None):
    # load task specific cfg
    parser = argparse.ArgumentParser()
    parser.add_argument('--nnodes',         type=int, default=1, help="num of host")
    parser.add_argument('--nproc_per_node', type=int, default=1, help="GPU per host")
    parser.add_argument('--node_rank',      type=int, default=0, help="rank of the host")
    parser.add_argument('--master_addr',    type=str, default='127.0.0.1', help="ip addr of the master server")
    parser.add_argument('--master_port',    type=str, default='23456', help="port ofthe master server")

    parser.add_argument("--eval_only", default=False, help="perform evaluation only")
    parser.add_argument(
        "--resume",
        default=False, 
        help="Whether to attempt to resume from the checkpoint directory. "
        "See documentation of `DefaultTrainer.resume_or_load()` for what it means.",
    )

    parser.add_argument('--exp_root', type=str)
    parser.add_argument('--config', type=str, default='config.yaml')

    parser.add_argument(
        "opts",
        help="Modify config options by adding 'KEY VALUE' pairs at the end of the command. "
             "See config references at "
             "https://detectron2.readthedocs.io/modules/config.html#config-references",
        default=None,
        nargs=argparse.REMAINDER,
    )

    return parser

def default_setup(cfg):
    #setup snapshot dir
    checkpoint_dir = os.path.join(cfg.EXPERIMENT.ROOT_DIR, cfg.EXPERIMENT.CHECKPOINT_DIR)

    if cfg.LAUNCH.GLOBAL_RANK == 0 and not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)

    #setup log dir
    log_dir = os.path.join(cfg.EXPERIMENT.ROOT_DIR, cfg.EXPERIMENT.LOG_DIR)
    if cfg.LAUNCH.GLOBAL_RANK == 0 and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # dir for tensorboard
    tb_dir = os.path.join(cfg.EXPERIMENT.ROOT_DIR, cfg.EXPERIMENT.TENSORBOARD_DIR)
    if cfg.LAUNCH.GLOBAL_RANK == 0 and not os.path.exists(tb_dir):
        os.makedirs(tb_dir)


class DefaultTrainer(TrainerBase):
    def __init__(self, cfg):
        super().__init__()

        self.logger = Logger(logger=__name__, level=logging.DEBUG)

        self.cfg = cfg

        self.setup_env()
        
        self.setup_seed()

        model = self.build_model(cfg)

        model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)

        data_loader = self.build_train_dataloader(cfg)

        optimizer = self.build_optimizer(cfg, model)
        
        model = create_ddp_model(model, find_unused_parameters=True, broadcast_buffers=False)

        self._trainer = (AMPTrainer if cfg.SOLVER.AMP.ENABLED else SimpleTrainer)(
            model, data_loader, optimizer
        )

        self.scheduler = self.build_lr_scheduler(cfg, optimizer)

        self.checkpointer = VCheckpointer(model, self.checkpoint_dir, trainer=weakref.proxy(self))

        self.iters_per_epoch = int(len(data_loader.dataset)/cfg.DATALOADER.BATCH_SIZE)
        self.start_iter = 0
        self.max_iter = int(cfg.EXPERIMENT.MAX_EPOCH * self.iters_per_epoch) + 1

        self.register_hooks(self.build_hooks())


    def setup_env(self):
        #setup snapshot dir
        self.checkpoint_dir = os.path.join(self.cfg.EXPERIMENT.ROOT_DIR, self.cfg.EXPERIMENT.CHECKPOINT_DIR)

        if self.cfg.LAUNCH.GLOBAL_RANK == 0 and not os.path.exists(self.checkpoint_dir):
            os.makedirs(self.checkpoint_dir)

        #setup log dir
        self.log_dir = os.path.join(self.cfg.EXPERIMENT.ROOT_DIR, self.cfg.EXPERIMENT.LOG_DIR)
        if self.cfg.LAUNCH.GLOBAL_RANK == 0 and not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # dir for tensorboard
        self.tb_dir = os.path.join(self.cfg.EXPERIMENT.ROOT_DIR, self.cfg.EXPERIMENT.TENSORBOARD_DIR)
        if self.cfg.LAUNCH.GLOBAL_RANK == 0 and not os.path.exists(self.tb_dir):
            os.makedirs(self.tb_dir)

    def setup_seed(self):
        if self.cfg.EXPERIMENT.SEED < 0:
            seed = (
                os.getpid()
                + int(datetime.now().strftime("%S%f"))
                + int.from_bytes(os.urandom(2), "big")
            )
        else:
            seed = self.cfg.EXPERIMENT.SEED + comm.get_rank()

        torch.manual_seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
            
        os.environ['PYTHONHASHSEED'] = str(seed)

        random.seed(seed)
        ##np.random.seed(self.cfg.EXPERIMENT.seed + self.cfg.LAUNCH.global_rank)
        np.random.seed(seed)

        torch.backends.cudnn.enabled = False
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True


    def resume_or_load(self):
        self.checkpointer.resume_or_load(self.cfg.MODEL.WEIGHTS, resume=self.cfg.EXPERIMENT.RESUME)
        if self.cfg.EXPERIMENT.RESUME and self.checkpointer.has_checkpoint():
            # The checkpoint stores the training iteration that just finished, thus we start
            # at the next iteration
            self.start_iter = self.iter + 1

    def build_hooks(self):
        cfg = self.cfg.clone()
        cfg.defrost()
        
        cfg.DATALOADER.WORKER_NUM = 0  # save some memory and time for PreciseBN

        ret = [
            hooks.IterationTimer(),
            hooks.LRScheduler(),
            #hooks.SetSamplerSeed(self.dataloader, self.iters_per_epoch)
            #hooks.ScheduledSampling(
            #    start_iter = cfg.SCHEDULED_SAMPLING.START_EPOCH * self.iters_per_epoch,
            #    inc_every_iter = cfg.SCHEDULED_SAMPLING.INC_EVERY_EPOCH * self.iters_per_epoch,
            #    inc_prob = cfg.SCHEDULED_SAMPLING.INC_PROB,
            #    max_prob = cfg.SCHEDULED_SAMPLING.MAX_PROB
            #),
        ]

        # Do PreciseBN before checkpointer, because it updates the model and need to
        # be saved by checkpointer.
        # This is not always the best: if checkpointing has a different frequency,
        # some checkpoints may have more precise statistics than others.
        if comm.is_main_process():
            ret.append(hooks.PeriodicCheckpointer(self.checkpointer,
                                                  cfg.SOLVER.CHECKPOINT_PERIOD * self.iters_per_epoch))
        
        def test_and_save_results(epoch):
            eval_results = self.test(self.cfg, self.model)
            return eval_results

        # Do evaluation after checkpointer, because then if it fails,
        # we can use the saved checkpoint to debug.

        ret.append(
            hooks.EvalHook(
                eval_period = cfg.EXPERIMENT.EVAL_PERIOD,
                eval_start = cfg.EXPERIMENT.EVAL_START,
                eval_function = test_and_save_results,
                iters_per_epoch = self.iters_per_epoch,
                stage = 'val',
                multi_gpu_eval=True
            ))
        

        if comm.is_main_process():
            ret.append(hooks.BestCheckpointer(cfg.SOLVER.CHECKPOINT_PERIOD * self.iters_per_epoch, self.checkpointer, "EVALUATE_STRING/acc"))


        if comm.is_main_process():
            # Here the default print/log frequency of each writer is used.
            # run writers in the end, so that evaluation metrics are written
            ret.append(hooks.PeriodicWriter(self.build_writers(), period=cfg.EXPERIMENT.LOG_PERIOD))

        return ret

    def build_writers(self):
        return default_writers(self.tb_dir, self.iters_per_epoch, self.max_iter)

    def train(self):
        """
        Run training.

        Returns:
            OrderedDict of results, if evaluation is enabled. Otherwise None.
        """
        super().train(self.start_iter, self.max_iter)

    def run_step(self):
        self._trainer.iter = self.iter
        self._trainer.run_step()
        

    def state_dict(self):
        ret = super().state_dict()
        ret["_trainer"] = self._trainer.state_dict()
        return ret

    def load_state_dict(self, state_dict):
        super().load_state_dict(state_dict)
        self._trainer.load_state_dict(state_dict["_trainer"])

    @classmethod
    def build_model(cls, cfg):
        """
        Returns:
            torch.nn.Module:
        It now calls :func:`detectron2.modeling.build_model`.
        Overwrite it if you'd like a different model.
        """
        model = build_model(cfg)
        return model

    @classmethod
    def build_optimizer(cls, cfg, model):
        return build_optimizer(cfg, model)

    @classmethod
    def build_lr_scheduler(cls, cfg, optimizer):
        return build_lr_scheduler(cfg, optimizer)

    @classmethod
    def build_train_dataloader(cls, cfg):
        """
        Returns:
            iterable
        """
        return build_train_dataloader(cfg)

    @classmethod
    def build_test_loader(cls, cfg, dataset_name=""):
        """
        Returns:
            iterable
        """
        return build_test_dataloader(cfg)

    @classmethod
    def build_evaluator(cls, cfg, dataset_name="", output_folder=None):
        """
        Returns:
            DatasetEvaluator or None
        """
        return build_evaluator(cfg)

    @classmethod
    def test(cls, cfg, model, evaluators=None):
        """
            Evaluate the given model. The given model is expected to already contain
            weights to evaluate.
            Args:
                cfg (CfgNode):
                model (nn.Module):
                evaluators (list[DatasetEvaluator] or None): if None, will call
                    :meth:`build_evaluator`. Otherwise, must have the same length as
                    ``cfg.DATASETS.TEST``.
            Returns:
                dict: a dict of result metrics
            """
        dataloader = cls.build_test_loader(cfg)

        evaluator = cls.build_evaluator(cfg)

        model.eval()

        with torch.no_grad():
            for batch_idx, in_batch in enumerate(dataloader):
                out_batch = model(in_batch)
                evaluator.process(in_batch, out_batch)

        result = evaluator.evaluate()

        model.train()

        return result


# Access basic attributes from the underlying trainer
for _attr in ["model", "data_loader", "optimizer"]:
    setattr(
        DefaultTrainer,
        _attr,
        property(
            # getter
            lambda self, x=_attr: getattr(self._trainer, x),
            # setter
            lambda self, value, x=_attr: setattr(self._trainer, x, value),
        ),
    )

