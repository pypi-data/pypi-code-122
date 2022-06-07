#!/usr/bin/env python3
import warnings
from typing import Any, List, Tuple, Union

import torch
import torch.nn.functional as F
from torch import Tensor
from torch.nn import Module
from torch.utils.hooks import RemovableHandle

from captum.attr._utils.attribution import GradientAttribution
from captum.attr._utils.common import _format_attributions, _format_input, _is_tuple
from captum.attr._utils.gradient import apply_gradient_requirements, undo_gradient_requirements
from captum.attr._utils.typing import TargetType, TensorOrTupleOfTensorsGeneric


class ModifiedReluGradientAttribution(GradientAttribution):
    def __init__(self, model: Module, use_relu_grad_output: bool = False):
        r"""
        Args:

            model (nn.Module):  The reference to PyTorch model instance.
        """
        GradientAttribution.__init__(self, model)
        self.model = model
        self.backward_hooks: List[RemovableHandle] = []
        self.activation_maps=[]
        self.use_relu_grad_output = use_relu_grad_output
        assert isinstance(self.model, torch.nn.Module), (
            "Given model must be an instance of torch.nn.Module to properly hook"
            " ReLU layers."
        )

    def attribute(
        self,
        inputs: TensorOrTupleOfTensorsGeneric,
        target: TargetType = None,
        additional_forward_args: Any = None,
    ) -> TensorOrTupleOfTensorsGeneric:
        r"""
        Computes attribution by overriding relu gradients. Based on constructor
        flag use_relu_grad_output, performs either GuidedBackpropagation if False
        and Deconvolution if True. This class is the parent class of both these
        methods, more information on usage can be found in the docstrings for each
        implementing class.
        """

        # Keeps track whether original input is a tuple or not before
        # converting it into a tuple.
        is_inputs_tuple = _is_tuple(inputs)

        inputs = _format_input(inputs)
        gradient_mask = apply_gradient_requirements(inputs)

        # set hooks for overriding ReLU gradients
        warnings.warn(
            "Setting backward hooks on ReLU activations."
            "The hooks will be removed after the attribution is finished"
        )

        for name, module in self.model.named_modules():
            self._register_hooks(module,name)
        #self.model.apply(self._register_hooks)

        gradients = self.gradient_func(
            self.forward_func, inputs, target, additional_forward_args
        )

        # remove set hooks
        self._remove_hooks()

        undo_gradient_requirements(inputs, gradient_mask)
        return _format_attributions(is_inputs_tuple, gradients)

    def _register_hooks(self, module: Module,name):
        #if 'layer4.2.relu2'==name.lower():
        #    print(name)
        if isinstance(module, torch.nn.ReLU) and 'layer4.2.relu2'!=name.lower():
            hook = module.register_backward_hook(self._backward_hook)
            self.backward_hooks.append(hook)
        if 'fc'== name.lower() or 'classifier.6' == name.lower():
            hook = module.register_backward_hook(self._backward_fc_hook)
            self.backward_hooks.append(hook)
            hook = module.register_forward_hook(self._forward_fc_hook)
            self.backward_hooks.append(hook)


    def _backward_hook(
        self,
        module: Module,
        grad_input: Union[Tensor, Tuple[Tensor, ...]],
        grad_output: Union[Tensor, Tuple[Tensor, ...]],
    ):
        to_override_grads = grad_output if self.use_relu_grad_output else grad_input
        if isinstance(to_override_grads, tuple):
            return tuple(
                F.relu(to_override_grad) for to_override_grad in to_override_grads
            )
        else:
            return F.relu(to_override_grads)
    def _backward_fc_hook(
        self,
        module: Module,
        grad_input: Union[Tensor, Tuple[Tensor, ...]],
        grad_output: Union[Tensor, Tuple[Tensor, ...]],
    ):
        to_override_grads = grad_input
        if isinstance(to_override_grads, tuple):
            return tuple(
                to_override_grad*self.activation_maps[0] if (to_override_grad.size()==self.activation_maps[0].size())
                else to_override_grad for to_override_grad in to_override_grads
            )
        else:
            return to_override_grads*self.activation_maps[0]
    def _forward_fc_hook(
        self,
        module: Module,
        input: Union[Tensor, Tuple[Tensor, ...]],
        output: Union[Tensor, Tuple[Tensor, ...]],
    ):
        #print(input)
        if isinstance(input,tuple):
            self.activation_maps.append(input[0])
        else:
            self.activation_maps.append(input)

    def _remove_hooks(self):
        for hook in self.backward_hooks:
            hook.remove()


class AIR(ModifiedReluGradientAttribution):
    r"""
    Computes attribution using guided backpropagation. Guided backpropagation
    computes the gradient of the target output with respect to the input,
    but gradients of ReLU functions are overridden so that only
    non-negative gradients are backpropagated.

    More details regarding the guided backpropagation algorithm can be found
    in the original paper here:
    https://arxiv.org/abs/1412.6806

    Warning: Ensure that all ReLU operations in the forward function of the
    given model are performed using a module (nn.module.ReLU).
    If nn.functional.ReLU is used, gradients are not overridden appropriately.
    """

    def __init__(self, model: Module):
        r"""
        Args:

            model (nn.Module):  The reference to PyTorch model instance.
        """
        ModifiedReluGradientAttribution.__init__(
            self, model, use_relu_grad_output=False
        )

    def attribute(
        self,
        inputs: TensorOrTupleOfTensorsGeneric,
        target: TargetType = None,
        module_name= 'fc',
        max_k=5,
        additional_forward_args: Any = None,
    ) -> TensorOrTupleOfTensorsGeneric:
        r"""
        Args:

            inputs (tensor or tuple of tensors):  Input for which
                        attributions are computed. If forward_func takes a single
                        tensor as input, a single input tensor should be provided.
                        If forward_func takes multiple tensors as input, a tuple
                        of the input tensors should be provided. It is assumed
                        that for all given input tensors, dimension 0 corresponds
                        to the number of examples (aka batch size), and if
                        multiple input tensors are provided, the examples must
                        be aligned appropriately.
            target (int, tuple, tensor or list, optional):  Output indices for
                        which gradients are computed (for classification cases,
                        this is usually the target class).
                        If the network returns a scalar value per example,
                        no target index is necessary.
                        For general 2D outputs, targets can be either:

                        - a single integer or a tensor containing a single
                          integer, which is applied to all input examples

                        - a list of integers or a 1D tensor, with length matching
                          the number of examples in inputs (dim 0). Each integer
                          is applied as the target for the corresponding example.

                        For outputs with > 2 dimensions, targets can be either:

                        - A single tuple, which contains #output_dims - 1
                          elements. This target index is applied to all examples.

                        - A list of tuples with length equal to the number of
                          examples in inputs (dim 0), and each tuple containing
                          #output_dims - 1 elements. Each tuple is applied as the
                          target for the corresponding example.

                        Default: None
            additional_forward_args (any, optional): If the forward function
                        requires additional arguments other than the inputs for
                        which attributions should not be computed, this argument
                        can be provided. It must be either a single additional
                        argument of a Tensor or arbitrary (non-tuple) type or a tuple
                        containing multiple additional arguments including tensors
                        or any arbitrary python types. These arguments are provided to
                        forward_func in order, following the arguments in inputs.
                        Note that attributions are not computed with respect
                        to these arguments.
                        Default: None

        Returns:
            *tensor* or tuple of *tensors* of **attributions**:
            - **attributions** (*tensor* or tuple of *tensors*):
                        The guided backprop gradients with respect to each
                        input feature. Attributions will always
                        be the same size as the provided inputs, with each value
                        providing the attribution of the corresponding input index.
                        If a single tensor is provided as inputs, a single tensor is
                        returned. If a tuple is provided for inputs, a tuple of
                        corresponding sized tensors is returned.

        Examples::

            >>> # ImageClassifier takes a single input tensor of images Nx3x32x32,
            >>> # and returns an Nx10 tensor of class probabilities.
            >>> net = ImageClassifier()
            >>> gbp = GuidedBackprop(net)
            >>> input = torch.randn(2, 3, 32, 32, requires_grad=True)
            >>> # Computes Guided Backprop attribution scores for class 3.
            >>> attribution = gbp.attribute(input, target=3)
        """
        return super().attribute(inputs, target, additional_forward_args)
        '''
        if hasattr(self.model, module_name):
            raw_weight = self.model.__getattr__(module_name).weight.data.clone()
            max_k = min(max_k, raw_weight.size(1))
        else:
            print('no such module')
        
        #==============================================
        def get_feature(inputs,model,module):
            mid=[]
            def hook_function(module, inputs, outputs):
                mid.append(inputs)

            hook=model.__getattr__(module_name).register_forward_hook(hook_function)
            _=model(inputs)
            hook.remove()
            return mid[0][0]
        feature=get_feature(inputs,self.model,self.model.__getattr__(module_name))
        #print(target)
        #print(raw_weight)
        tt=raw_weight[target]
        #print(feature)
        contribution=feature.data*tt
        
        mid_value,mid_list=torch.topk(contribution,max_k)
        #print(mid_value)
        # =======================================
        inputs_list=torch.split(inputs,1)
        target_list=torch.split(target,1)
        final_result=[]
        
        for i in range(len(inputs_list)):
            result=[]
            for k in range(mid_list.size(1)):
                temp = torch.zeros_like(raw_weight)
                temp[:, mid_list[i,k]] = 1
                self.model.__getattr__(module_name).weight.data=temp
                #print(inputs_list[i].size(),target_list[i])
                tt=torch.abs(super().attribute(inputs_list[i], target_list[i], additional_forward_args))
                #print(tt)
                result.append(tt)
            #=============================================
            self.model.__getattr__(module_name).weight.data = raw_weight
            result=torch.cat(result,0)

            tt=torch.zeros_like(mid_value[i].view(-1,1,1,1))
            tt[0]=1
            #print(tt.size(), result.size())
            final_result.append(torch.sum(tt*result,0,keepdim=True))
        final_result=torch.cat(final_result,0)
        
        return final_result
        '''


