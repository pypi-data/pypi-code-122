# Copyright (c) OpenMMLab. All rights reserved.
import copy
import inspect
from collections import OrderedDict
from typing import Optional, Union

import poptorch
import torch
import torch.nn as nn
from poptorch import PoplarExecutor, __version__, identity_loss
from poptorch._args_parser import ArgsParser

from mmcv.runner import auto_fp16
from .hierarchical_data_manager import HierarchicalDataManager
from .utils import compare_ndarray, model_sharding, recomputation_checkpoint


class DictArgsParser(ArgsParser):
    """A helper class for handling model input.

    Args:
        inputs (list): Inputs of model.
    """

    def __init__(self, inputs):
        # Combine args and kwargs:
        self._has_variadic_arguments = True
        self._varnames = list(inputs.keys())
        self._defaults = [inspect.Parameter.empty for _ in self._varnames]
        self._warned_not_contiguous_input = False


class WrappedNet(nn.Module):
    """A net wrapper for model conversion.

    This wrapper will make some changes and add some extra functions to
    training/inference model.

    Args:
        model (:obj:`nn.Module`): The model to run.
        inputs_manager (:obj:`HierarchicalDataManager`): A parser
            converting inputs from tuple to dictionary.
        outputs_manager (:obj:`HierarchicalDataManager`): A parser
            converting outputs from dictionary to tuple.
        inter_outputs_in_cpu (dict): Specify the features to be
            recorded.
        modules_to_record (mmcv.Config, list): Index or name of modules which
            will be recorded for output. It is necessary to specify output for
            static graph of model training or inference.
    """

    def __init__(self,
                 model,
                 inputs_manager,
                 outputs_manager,
                 inter_outputs_in_cpu,
                 modules_to_record=None):
        super().__init__()
        self.model = model
        self.inputs_manager = inputs_manager
        self.outputs_manager = outputs_manager
        self.training = model.training
        # Register a hook function to capture the intermediate features
        # generated by the network to align the outputs between ipu and cpu
        # Used to confirm whether the implementation of CPU is consistent
        # with the implementation of IPU
        self.inter_outputs_in_cpu = inter_outputs_in_cpu
        if modules_to_record is None:
            modules_to_record = []

        for idx, (name, module) in enumerate(model.named_modules()):
            if name in modules_to_record or idx in modules_to_record:
                features_hook = self.get_input_output_hook(
                    name, idx, self.inter_outputs_in_cpu)
                module.register_forward_hook(hook=features_hook)

    def get_input_output_hook(self, name, idx, save_dict):

        def input_output_hook(module, fea_in, fea_out):
            if isinstance(fea_in, tuple):
                fea_in = list(fea_in)
            if isinstance(fea_out, tuple):
                fea_out = list(fea_out)
            save_dict[name] = {
                'fea_in': fea_in,
                'fea_out': fea_out,
                'idx': idx
            }
            return None

        return input_output_hook

    def forward(self, inputs_tuple):
        """This function is used to be compiled to ipu, the inputs and outputs
        need to be tuples, so here we need to restore the input back to a
        dictionary and convert the output to a tuple."""
        self.inputs_manager.update_all_tensors(inputs_tuple)
        kwargs = {**(self.inputs_manager.hierarchical_data)}
        if self.training:
            outputs = self.forward_train(kwargs)
            # tell poptorch which loss will be used finally
            identity_loss(outputs['loss'], reduction='none')
        else:
            outputs = self.forward_eval(kwargs)

        if isinstance(outputs, torch.Tensor):
            # currently not support single tensor output,
            # need to wrap it with a dictionary,
            # use a keyword to identify this case
            outputs = {'output of WrappedNet: single tensor': outputs}

        # if there are some features need to be record, add extra outputs
        for name in self.inter_outputs_in_cpu:
            outputs[name] = self.inter_outputs_in_cpu[name]

        # record all the places of return tensors in the converting stage
        # while in the real run stage, all the tensor are changed in-place
        # that means the output can be obtained directly outside this function
        self.outputs_manager.record_hierarchical_data(outputs)
        plain_outputs = self.outputs_manager.collect_all_tensors()
        return plain_outputs

    def forward_train(self, kwargs):
        optimizer = kwargs.pop('optimizer')
        outputs = self.train_step(kwargs, optimizer)
        return outputs

    def train_step(self, data, optimizer=None, **kwargs):
        """The iteration step during training.

        This method defines an iteration step during training, except for the
        back propagation and optimizer updating, which are done in an optimizer
        hook. Note that in some complicated cases or models, the whole process
        including back propagation and optimizer updating are also defined in
        this method, such as GAN.

        Args:
            data (dict): The output of dataloader.
            optimizer (:obj:`torch.optim.Optimizer`, optional): The
                optimizer of runner is passed to ``train_step()``. This
                argument is unused and reserved.

        Returns:
            dict: Dict of outputs. The following fields are contained.
                - loss (torch.Tensor): A tensor for back propagation, which \
                    can be a weighted sum of multiple losses.
                - log_vars (dict): Dict contains all the variables to be sent \
                    to the logger.
                - num_samples (int): Indicates the batch size (when the model \
                    is DDP, it means the batch size on each GPU), which is \
                    used for averaging the logs.
        """
        losses = self.model(**data)
        loss, log_vars = self._parse_losses(losses)

        outputs = dict(
            loss=loss, log_vars=log_vars, num_samples=len(data['img'].data))

        return outputs

    def _parse_losses(self, losses):
        log_vars = OrderedDict()
        for loss_name, loss_value in losses.items():
            if isinstance(loss_value, torch.Tensor):
                log_vars[loss_name] = loss_value.mean()
            elif isinstance(loss_value, list):
                log_vars[loss_name] = sum(loss.mean() for loss in loss_value)
            elif isinstance(loss_value, dict):
                for name, value in loss_value.items():
                    log_vars[name] = value
            else:
                raise TypeError(
                    f'{loss_name} is not a tensor or list of tensors')

        loss = sum(value for key, value in log_vars.items() if 'loss' in key)
        log_vars['loss'] = loss

        return loss, log_vars

    def forward_eval(self, kwargs):
        img = kwargs.pop('img')
        img_metas = kwargs.pop('img_metas', None)
        return_loss = kwargs.pop('return_loss')
        assert not return_loss
        # TODO Temporarily hard-code to close post_process,
        # otherwise, in the third trace(_check_trace),
        # post_process will convert output tensor to numpy array automatically,
        # resulting in _check_trace failure
        outputs = self.model(
            img,
            img_metas=img_metas,
            return_loss=return_loss,
            post_process=False)
        return outputs


class MMPoplarExecutor(PoplarExecutor):
    """An executor for inputs/outputs parsing, model compilation, data
    alignment and IPU upload/download.

    Args:
        model (:obj:`nn.Module`): The model to be compiled.
        logger (:obj:`logging.Logger`): Logger used during running.
             Defaults to None.
        training (bool): Model in training mode or eval mode.
        modules_to_record (mmcv.Config, list): Index or name of modules which
            will be recorded for output. It is necessary to specify output for
            static graph of model training or inference.
        args (argument list): Arguments passed to the `__init__`
            method of PoplarExecutor.
        kwargs (keyword arguments): Keyword arguments passed to the `__init__`
            method of PoplarExecutor.
    """

    def __init__(self,
                 model,
                 logger=None,
                 training=True,
                 modules_to_record=None,
                 *args,
                 **kwargs):
        # self.model == self._user_model: input pytorch model
        # self._model: wrapped model which is used to compile
        # and update weights, these two models use same weights
        # wrapped model only accept and output tuple, so
        # HierarchicalDataManager will convert dictionary
        # to tuple and convert them back
        self.inputs_manager = HierarchicalDataManager(logger=logger)
        self.outputs_manager = HierarchicalDataManager(logger=logger)
        self.logger = logger
        # the features calculated by CPU
        self.inter_outputs_in_cpu = {}
        # the features calculated by IPU
        self.inter_outputs_in_ipu = {}
        if modules_to_record is None:
            # It is possible that the IPU implementation of some operators
            # is inconsistent with the expected (CPU), here you can use
            # this method to confirm whether there is a problem
            self.compare_with_cpu = False
        else:
            self.compare_with_cpu = True
        # move model.fp16_enabled to self.fp16_enabled,
        # modify the position where the input is automatically casted to half
        if getattr(model, 'fp16_enabled', False):
            model.fp16_enabled = False
            self.fp16_enabled = True
        # make torch.jit.trace convert self._model
        model = WrappedNet(
            model,
            self.inputs_manager,
            self.outputs_manager,
            self.inter_outputs_in_cpu,
            modules_to_record=modules_to_record)
        super().__init__(model, training=training, *args, **kwargs)
        # overwrite self._args_parser in train_step or val_step
        self._args_parser = None
        if training:
            assert self.training
        else:
            assert not self.training

    @property
    def training(self):
        # If trying to get the attribute(training) of self,
        # since the class has no training attribute,
        # it will automatically look for the training attribute of self.model.
        # However, the real attribute we want to check is self._training,
        # self.model.training  and self._training are often inconsistent.
        # It is not clear whether it is a Poptorch bug or a special design,
        # temporarily use this function to fix the problem
        return self._training  # comes from self.model._training

    @auto_fp16(supported_types=(PoplarExecutor, ))
    def run_model(self, data_dict):
        # this function is used to parse input_dict
        # and convert to output_dict
        if self.isCompiled():
            self.inputs_manager.record_hierarchical_data(data_dict)
            inputs_tuple = tuple(self.inputs_manager.collect_all_tensors())
        else:
            # get tensors out of data and put them in a tuple
            self.inputs_manager.record_hierarchical_data(data_dict)
            inputs_tuple = tuple(self.inputs_manager.collect_all_tensors())
            # turn logger in data manager off after compilation
            self.inputs_manager.quick()
            self.outputs_manager.quick()

        # parser args in the first iter
        if self._args_parser is None:
            self._args_parser = DictArgsParser({'args': inputs_tuple})

        # run or convert model
        # the plain_outputs will be used in converting stage
        plain_outputs = self(inputs_tuple)

        self.inputs_manager.clean_all_tensors()

        # put list of tensors back to the output dict
        # according to the same order
        self.outputs_manager.update_all_tensors(plain_outputs)
        # get the real output dictionary from self.outputs_manager
        output_dict = self.outputs_manager.hierarchical_data

        # split output_dict into inter_outputs_in_ipu
        # and output of the torch model
        torch_model_output = {}
        for name in output_dict:
            if name in self.inter_outputs_in_cpu:
                self.inter_outputs_in_ipu[name] = output_dict[name]
            else:
                torch_model_output[name] = output_dict[name]

        if 'output of WrappedNet: single tensor' in output_dict:
            assert len(torch_model_output) == 1
            assert isinstance(
                torch_model_output['output of WrappedNet: single tensor'],
                torch.Tensor)
            torch_model_output = \
                torch_model_output['output of WrappedNet: single tensor']

        return torch_model_output

    def train_step(self, data, optimizer=None, **kwargs):
        # arguments from mmcls/models/classifiers/base.py:
        # BaseClassifier.train_step
        assert self.training
        assert len(kwargs) == 0  # TODO, support later if necessary

        # TODO support datacontainer as input
        # currently, auto_fp16 and HierarchicalDataManager take too much
        # time on traversing datacontainer
        data['img_metas'] = None
        num_samples = len(data['img'].data)

        # TODO we will ignore optimizer because it will not be used in model,
        # support later if necessary
        data['optimizer'] = None
        output_dict = self.run_model(data)

        # outputs contained loss, log_vars, num_samples,
        # only loss(torch.tensor) has been updated
        # remove all unchanged vars, left torch.tensor
        neat_output_dict = {'loss': output_dict['loss']}

        # re-parse outputs, get back log_vars and num_samples
        loss, log_vars = self.model._parse_losses(neat_output_dict)
        final_output_dict = dict(
            loss=loss, log_vars=log_vars, num_samples=num_samples)
        return final_output_dict

    def eval_call(self, img, img_metas=None, return_loss=True, **kwargs):
        # arguments from mmdet/models/detectors/base.py:BaseDetector.forward
        # tmp usssage for eval mode
        assert not self.training
        assert len(kwargs) == 0  # TODO, support later if necessary
        assert not return_loss
        data = {'img': img, 'img_metas': img_metas, 'return_loss': return_loss}

        output_dict = self.run_model(data)

        return output_dict

    def detachFromDevice(self):
        if self.isCompiled() and self._is_attached:
            super().detachFromDevice()

    def attachToDevice(self):
        if self.isCompiled() and not self._is_attached:
            super().attachToDevice()


class TrainEvalModel:
    """A class maintaining training MMPoplarExecutor and inference
    MMPoplarExecutor.

    Args:
        train_model (:obj:`nn.Module`): The training model to be compiled.
            ``train_model`` can be None if only executing validation.
        eval_model (:obj:`nn.Module`): The inference model to be compiled.
        options (mmcv.Config, dict): Options that will be used to compile
            and run the model.
        optimizer (:obj:`torch.optim.Optimizer`, optional): torch
            optimizer, necessary if in training mode
        logger (:obj:`logging.Logger`): Logger used during running.
             Defaults to None.
        modules_to_record (mmcv.Config, list): Index or name of modules which
            will be recorded for output. It is necessary to specify output for
            static graph of model training or inference.
    """

    def __init__(self,
                 train_model,
                 eval_model,
                 options,
                 optimizer,
                 modules_to_record=None,
                 logger=None):
        if train_model is None:
            self._train_executor = None
            self.training = False
        else:
            self._train_executor = get_training_model(
                train_model,
                options=options['training'],
                optimizer=optimizer,
                logger=logger,
                modules_to_record=modules_to_record)
            self.training = True
        self._eval_executor = get_inference_model(
            eval_model, options=options['inference'], logger=logger)

    @property
    def executor(self):
        if self.training:
            return self._train_executor
        else:
            return self._eval_executor

    def train(self, mode: bool = True):
        """Sets the module in training mode.

        This has any effect only on certain modules. See documentations of
        particular modules for details of their behaviors in
        training/evaluation mode, if they are affected,
        e.g. :class:`Dropout`, :class:`BatchNorm`, etc.

        Args:
            mode (bool): whether to set training mode (``True``) or evaluation
                mode (``False``). Default: ``True``.

        Returns:
            Module: self
        """
        if not isinstance(mode, bool):
            raise ValueError('training mode is expected to be boolean, '
                             f'but got {type(mode)}')
        if self._train_executor is None and mode:
            raise RuntimeError(
                'The train_executor is not initialized.'
                'If you want to initialize train_executor,'
                'you need to input optimizer when converting pytorch model')

        if mode == self.training:
            self.model.train(mode)
            return self
        else:
            if self.isCompiled():
                # copy weights from IPU to cpu before off-load current session
                self.copyWeightsToHost()
                # detach the current session before change the mode,
                # if is training mode and weights are updated,
                # poptorch will copy weights from IPU to host
                self.detachFromDevice()

            self.training = mode  # session will changed with mode changing
            self.model.train(mode)

            # after changing mode, attach the current new session,
            # and this function will copy weights of model to device
            self.attachToDevice()
            return self

    def eval(self):
        """Sets the module in evaluation mode.

        This has any effect only on certain modules.
        See documentations of particular modules
        for details of their behaviors in training/evaluation mode,
        if they are affected, e.g. :class:`Dropout`, :class:`BatchNorm`, etc.

        This is equivalent with :meth:`self.train(False)
        <nn.Module.train>`.

        See :ref:`locally-disable-grad-doc` for a comparison between
        `.eval()` and several similar mechanisms that may be confused with it.

        Returns:
            Module: self
        """
        return self.train(False)

    def compare_data_between_ipu_and_cpu(self, inter_outputs_in_cpu,
                                         inter_outputs_in_ipu):
        for key, val in inter_outputs_in_cpu.items():
            is_tensor = isinstance(val['fea_in'], torch.Tensor)
            fea_in_cpu = val['fea_in']
            fea_in_cpu_list = [fea_in_cpu] if is_tensor else fea_in_cpu
            fea_in_ipu = inter_outputs_in_ipu[key]['fea_in']
            fea_in_ipu_list = [fea_in_ipu] if is_tensor else fea_in_ipu

            is_tensor = isinstance(val['fea_out'], torch.Tensor)
            fea_out_cpu = val['fea_out']
            fea_out_cpu_list = [fea_out_cpu] if is_tensor else fea_out_cpu
            fea_out_ipu = inter_outputs_in_ipu[key]['fea_out']
            fea_out_ipu_list = [fea_out_ipu] if is_tensor else fea_out_ipu

            print('comparing layer:', key)
            for idx, (featA, featB) in \
                    enumerate(zip(fea_in_cpu_list, fea_in_ipu_list)):
                print('fea_in, tensor ', idx)
                compare_ndarray(featA.detach().numpy(), featB.detach().numpy())
            for idx, (featA, featB) in \
                    enumerate(zip(fea_out_cpu_list, fea_out_ipu_list)):
                print('fea_out, tensor', idx)
                compare_ndarray(featA.detach().numpy(), featB.detach().numpy())

    # TODO Unified training and eval interface,
    # merge train_step(train) and __call__(eval) together
    def train_step(self, data, optimizer=None, **kwargs):
        assert self.training, 'not supported train_step on eval mode'
        inter_outputs_in_cpu = {}
        if (self._train_executor.isCompiled()
                and self._train_executor.compare_with_cpu):
            self.copyWeightsToHost()
            # run in CPU mode
            self._train_executor.model.train_step(data, optimizer, **kwargs)
            inter_outputs_in_cpu = {
                **(self._train_executor.inter_outputs_in_cpu)
            }
        # run in IPU mode
        result = self._train_executor.train_step(data, optimizer, **kwargs)
        if (self._train_executor.isCompiled()
                and self._train_executor.compare_with_cpu
                and len(inter_outputs_in_cpu) > 0):
            self.compare_data_between_ipu_and_cpu(
                inter_outputs_in_cpu,
                self._train_executor.inter_outputs_in_ipu)
        return result

    # TODO Unified training and eval interface,
    # merge train_step(train) and __call__(eval) together
    def __call__(self, *args, **kwargs):
        if self.training:
            raise NotImplementedError('use train_step rather than __call__')
        else:
            return self._eval_executor.eval_call(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.executor, attr)


def get_training_model(model: nn.Module,
                       options: Optional[poptorch.Options] = None,
                       optimizer: Optional[torch.optim.Optimizer] = None,
                       logger=None,
                       modules_to_record=None) -> poptorch.PoplarExecutor:
    """Create a PopTorch training model from a PyTorch model, running on IPU
    hardware in training mode.

    Note:
        PopTorch makes a shallow copy of the model. Changes to the
        parameters in the returned training model affect the original model
        and vice versa. However, primitive variable types are not synced: for
        example calling ``model.train()`` on the original model, which
        changes the ``training`` bool of the model instance, will not alter the
        model returned by this function. You may need to call ``model.train()``
        on your model before you call this function for correct behavior.

    Args:
        model (:obj:`nn.Module`): The model to run.
        options (poptorch.Options): Options that will be used to compile
            and run the model.
        optimizer (:obj:`torch.optim.Optimizer`, optional): The optimizers
            to apply during training.
        logger (:obj:`logging.Logger`): Logger used during running.
             Defaults to None.
        modules_to_record (mmcv.Config, list): Index or name of modules which
            will be recorded for output. It is necessary to specify output for
            static graph of model training or inference.

    Returns:
        The :class:`poptorch.PoplarExecutor` wrapper to use in place
        of ``model``.
    """
    # Create a copy of the original model in case it needs to be wrapped
    maybe_wrapped_model = copy.copy(model)

    return MMPoplarExecutor(
        model=maybe_wrapped_model,
        logger=logger,
        options=options,
        training=True,
        optimizer=optimizer,
        user_model=model,
        modules_to_record=modules_to_record,
        poptorch_version=__version__)


def get_inference_model(model: Union[nn.Module, poptorch.PoplarExecutor],
                        options: Optional[poptorch.Options] = None,
                        logger=None) -> poptorch.PoplarExecutor:
    """Create a PopTorch inference model from a PyTorch model, running on IPU
    hardware in inference mode.

    Note:
        PopTorch makes a shallow copy of the model. Changes to the
        parameters in the returned inference model affect the original model
        and vice versa. However, primitive variable types are not synced: for
        example calling ``model.eval()`` on the original model will not alter
        the model returned by this function. You may need to call
        ``model.eval()`` on your model before you call this function for
        correct behavior.

    Args:
        model (:obj:`nn.Module`): The model to run.
        options (poptorch.Options): Options that will be used to compile
            and run the model.
        logger (:obj:`logging.Logger`): Logger used during running.
             Defaults to None.

    Returns:
        The :class:`poptorch.PoplarExecutor` wrapper to use in place of
        ``model``.
    """

    return MMPoplarExecutor(
        model=copy.copy(model),
        logger=logger,
        options=options,
        training=False,
        poptorch_version=__version__)


def ipu_model_wrapper(model,
                      options,
                      optimizer=None,
                      logger=None,
                      modules_to_record=None,
                      ipu_model_cfg=None,
                      fp16_cfg=None):
    """Convert torch model to IPU model.

    Args:
        model (nn.Module): The target model to be converted.
        options (dict[str, poptorch.Options]): IPU options, generated
            by :func:`cfg2options`.
        optimizer (:obj:`torch.optim.Optimizer`, optional): torch
            optimizer, necessary if in training mode
        logger (:obj:`logging.Logger`): Logger used during training.
        modules_to_record (mmcv.Config, list): Index or name of modules which
            will be recorded for output. It is necessary to specify output for
            static graph of model training or inference.
        ipu_model_cfg (dict): A dictionary contains train_split_edges and
            train_ckpt_nodes, See details in :func:`model_sharding` and
            :func:`recomputation_checkpoint` functions.
        fp16_cfg (dict): Config for IPU fp16 training. Currently supports
            configs: `loss_scale`, `velocity_accum_type` and `accum_type`.
            See details in
            https://docs.graphcore.ai/projects/poptorch-user-guide/en/latest/index.html

    Returns:
        TrainEvalModel: IPU wrapped model.
    """
    if ipu_model_cfg is None:
        ipu_model_cfg = {}
    training = model.training if optimizer is not None else False
    # set mixed-precision
    if fp16_cfg is not None:
        from mmcv.runner import wrap_fp16_model
        loss_scale = fp16_cfg['loss_scale']
        wrap_fp16_model(model)
        model.half()
        # TODO tmp ussage to set loss scaling for torch original optimizer
        if optimizer is not None:
            optimizer.loss_scaling = loss_scale
            if fp16_cfg.get('velocity_accum_type', False):
                if fp16_cfg['velocity_accum_type'] == 'half':
                    optimizer.velocity_accum_type = torch.half
                else:
                    optimizer.velocity_accum_type = torch.float32
            if fp16_cfg.get('accum_type', False):
                if fp16_cfg['accum_type'] == 'half':
                    optimizer.accum_type = torch.half
                else:
                    optimizer.accum_type = torch.float32
        # TODO support feature alignment for fp16
        if modules_to_record is not None:
            raise NotImplementedError(
                'Feature alignment for fp16 is not implemented')

    # set model partition
    if optimizer is None:
        train_model = None
    else:
        # split model into multi-IPUs if specified
        train_model = model_sharding(
            copy.copy(model).train(),
            ipu_model_cfg.get('train_split_edges', []))

        recomputation_checkpoint(train_model,
                                 ipu_model_cfg.get('train_ckpt_nodes', []))

        # TODO support feature alignment for gradient accumulation mode
        gradient_accumulation = \
            getattr(options['training'].Training, 'gradient_accumulation', 1)
        if gradient_accumulation > 1:
            assert modules_to_record is None, \
                'Feature alignment for grad-accumulation mode not implemented'

        # TODO support feature alignment for multi-replica mode
        replication_factor = \
            getattr(options['training'], 'replication_factor', 1)
        if replication_factor > 1:
            assert modules_to_record is None, \
                'Feature alignment for multi-replica mode not implemented'

    # TODO supports different model partitions between train and eval mode
    assert len(ipu_model_cfg.get('eval_split_edges', [])) == 0,\
        'Currently, BeginBlock can only be used once on the same model'
    eval_model = copy.copy(model).eval()

    # wrap model for compilation
    model = TrainEvalModel(
        train_model,
        eval_model,
        options=options,
        optimizer=optimizer,
        logger=logger,
        modules_to_record=modules_to_record)
    model.train(training)
    return model
