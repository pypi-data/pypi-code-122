# -*- coding : utf-8 -*-
# @Time   : 2021/10/7 23:22
# @Author : goodli
# @File   : base.py
# @Project: Valley 山谷

from torch.utils.data.distributed import DistributedSampler
from torch.utils.data.dataloader import DataLoader

from yacs.config import CfgNode
from valley.utils.plugin import reg_plugin, get_plugin, PluginType
from valley.data.dataset import build_dataset
from valley.data import DataPhase
from valley.data.samplers import  TrainingSampler, InferenceSampler
from valley.config.config import configurable
from valley.utils import comm

@reg_plugin(PluginType.DATALOADER, "DefaultDataLoader")
class DefaultDataLoader(DataLoader):
    @configurable
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    @classmethod
    def from_config(cls, cfg, phase):
        dataset = build_dataset(cfg, phase)
        if phase == DataPhase.TRAIN:
            sampler = TrainingSampler(len(dataset))
            return {
                "dataset": dataset,
                "batch_size": int(cfg.DATALOADER.BATCH_SIZE/comm.get_world_size()),
                "shuffle": False,
                "num_workers": cfg.DATALOADER.WORKER_NUM,
                "pin_memory": True,
                "drop_last": False,
                "sampler": sampler
            }

        else:
            sampler = InferenceSampler(len(dataset))
            return {
                "dataset": dataset,
                "batch_size": int(cfg.DATALOADER.BATCH_SIZE),
                "shuffle": False,
                "num_workers": cfg.DATALOADER.WORKER_NUM,
                "pin_memory": True,
                "drop_last": False,
                "sampler": sampler
            }



