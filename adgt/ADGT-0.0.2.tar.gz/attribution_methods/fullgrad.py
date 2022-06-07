#

# Copyright (c) 2019 Idiap Research Institute, http://www.idiap.ch/

# Written by Suraj Srinivas <suraj.srinivas@idiap.ch>

#


""" Implement FullGrad saliency algorithm """

import torch

import torch.nn as nn

import torch.nn.functional as F

from math import isclose



class FullGradExtractor:

    # Extract tensors needed for FullGrad using hooks

    def __init__(self, model, no_grad=True, im_size=(3, 224, 224)):

        self.model = model

        self.im_size = im_size

        self.biases = []

        self.feature_grads = []

        self.grad_handles = []

        self.gbp_handles=[]

        self.no_grad=no_grad

        # Iterate through layers

        for m in self.model.modules():

            if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear) or isinstance(m, nn.BatchNorm2d):

                # Register feature-gradient hooks for each layer

                handle_g = m.register_backward_hook(self._extract_layer_grads)

                self.grad_handles.append(handle_g)

                # Collect model biases

                b = self._extract_layer_bias(m)

                if (b is not None): self.biases.append(b)
        self.model.apply(self._register_hooks)


    def _register_hooks(self, module):
        if isinstance(module, torch.nn.ReLU) or isinstance(module, torch.nn.Softplus):
            hook = module.register_backward_hook(self._backward_hook)
            self.gbp_handles.append(hook)

    def _backward_hook( self,  module, grad_input,  grad_output,    ):
        to_override_grads = grad_input
        act=F.relu
        #act= torch.nn.Softplus(beta=1000)
        if isinstance(to_override_grads, tuple):
            return tuple(
                act(to_override_grad) for to_override_grad in to_override_grads
            )
        else:
            return act(to_override_grads)

    def _extract_layer_bias(self, module):

        # extract bias of each layer

        # for batchnorm, the overall "bias" is different

        # from batchnorm bias parameter.

        # Let m -> running mean, s -> running std

        # Let w -> BN weights, b -> BN bias

        # Then, ((x - m)/s)*w + b = x*w/s + (- m*w/s + b)

        # Thus (-m*w/s + b) is the effective bias of batchnorm

        if isinstance(module, nn.BatchNorm2d):

            b = - (module.running_mean * module.weight

                   / torch.sqrt(module.running_var + module.eps)) + module.bias

            return b.data

        elif module.bias is None:

            return None

        else:

            return module.bias.data

    def getBiases(self):

        # dummy function to get biases

        return self.biases

    def _extract_layer_grads(self, module, in_grad, out_grad):

        # function to collect the gradient outputs

        # from each layer

        if not module.bias is None:
            self.feature_grads.append(out_grad[0])

    def getFeatureGrads(self, x, output_scalar):

        # Empty feature grads list

        self.feature_grads = []

        self.model.zero_grad()

        # Gradients w.r.t. input

        input_gradients = torch.autograd.grad(outputs=output_scalar, inputs=x,create_graph=not self.no_grad)[0]

        return input_gradients, self.feature_grads


class FullGrad():
    """

    Compute FullGrad saliency map and full gradient decomposition

    """

    def __init__(self, model, no_grad=True,im_size=(3, 224, 224)):

        self.model = model

        self.im_size = (1,) + im_size

        self.model_ext = FullGradExtractor(model, no_grad,im_size)

        self.biases = self.model_ext.getBiases()

        #self.checkCompleteness()

    def checkCompleteness(self):

        """

        Check if completeness property is satisfied. If not, it usually means that

        some bias gradients are not computed (e.g.: implicit biases of non-linearities).



        """

        cuda = torch.cuda.is_available()

        device = torch.device("cuda" if cuda else "cpu")

        # Random input image

        input = torch.randn(self.im_size).to(device)

        # Get raw outputs

        self.model.eval()

        raw_output = self.model(input)

        # Compute full-gradients and add them up

        input_grad, bias_grad = self.fullGradientDecompose(input, target_class=None)

        fullgradient_sum = (input_grad * input).sum()

        for i in range(len(bias_grad)):
            fullgradient_sum += bias_grad[i].sum()

        # Compare raw output and full gradient sum

        err_message = "\nThis is due to incorrect computation of bias-gradients."

        err_string = "Completeness test failed! Raw output = " + str(
            raw_output.max().item()) + " Full-gradient sum = " + str(fullgradient_sum.item())

        assert isclose(raw_output.max().item(), fullgradient_sum.item(), rel_tol=1e-4), err_string + err_message

        print('Completeness test passed for FullGrad.')

    def fullGradientDecompose(self, image, target_class=None):

        """

        Compute full-gradient decomposition for an image

        """

        self.model.eval()
        #print(image)
        image = image.requires_grad_()

        out = self.model(image)

        if target_class is None:
            target_class = out.data.max(1, keepdim=True)[1]

        # Select the output unit corresponding to the target class

        # -1 compensates for negation in nll_loss function

        output_scalar = -1. * F.nll_loss(out, target_class.flatten(), reduction='sum')

        input_gradient, feature_gradients = self.model_ext.getFeatureGrads(image, output_scalar)

        # Compute feature-gradients \times bias

        bias_times_gradients = []

        L = len(self.biases)

        for i in range(L):
            # feature gradients are indexed backwards

            # because of backprop

            g = feature_gradients[L - 1 - i]

            # reshape bias dimensionality to match gradients

            bias_size = [1] * len(g.size())

            bias_size[1] = self.biases[i].size(0)

            b = self.biases[i].view(tuple(bias_size))

            bias_times_gradients.append(g* b.expand_as(g))

        return input_gradient, bias_times_gradients

    def fullGradientDecompose_condition(self, image):

        """

        Compute full-gradient decomposition for an image

        """

        self.model.eval()
        #print(image)
        image = image.requires_grad_()

        out = self.model(image)

        # Select the output unit corresponding to the target class

        output_scalar =torch.sum(out)

        input_gradient, feature_gradients = self.model_ext.getFeatureGrads(image, output_scalar)

        # Compute feature-gradients \times bias

        bias_times_gradients = []

        L = len(self.biases)

        for i in range(L):
            # feature gradients are indexed backwards

            # because of backprop

            g = feature_gradients[L - 1 - i]

            # reshape bias dimensionality to match gradients

            bias_size = [1] * len(g.size())

            bias_size[1] = self.biases[i].size(0)

            b = self.biases[i].view(tuple(bias_size))

            bias_times_gradients.append(g* b.expand_as(g))

        return input_gradient, bias_times_gradients

    def _postProcess(self, input, eps=1e-6):

        # Absolute value
        '''
        input = abs(input)

        # Rescale operations to ensure gradients lie between 0 and 1

        flatin = input.view((input.size(0), -1))

        temp, _ = flatin.min(1, keepdim=True)

        input = input - temp.unsqueeze(1).unsqueeze(1)

        flatin = input.view((input.size(0), -1))

        temp, _ = flatin.max(1, keepdim=True)

        input = input / (temp.unsqueeze(1).unsqueeze(1) + eps)
        '''
        return input

    def attribute(self, image, target=None):

        # FullGrad saliency

        self.model.eval()

        input_grad, bias_grad = self.fullGradientDecompose(image, target_class=target)

        # Input-gradient * image

        grd = torch.clamp(input_grad*torch.sign(torch.abs(image)) /(image+1e-8),min=0,max=1)

        #gradient = self._postProcess(grd).sum(1, keepdim=True)

        #cam = gradient
        cam=grd.sum(1, keepdim=True)
        #cam=0
        im_size = image.size()

        # Aggregate Bias-gradients

        for i in range(len(bias_grad)):

            # Select only Conv layers

            if len(bias_grad[i].size()) == len(im_size):
                temp = self._postProcess(bias_grad[i])

                gradient = F.interpolate(temp, size=(im_size[2], im_size[3]), mode='bilinear', align_corners=True)

                cam += gradient.sum(1, keepdim=True)

        return cam

    def get_condition(self, image):

        # FullGrad saliency

        self.model.eval()

        input_grad, bias_grad = self.fullGradientDecompose_condition(image)

        # Input-gradient * image

        grd = input_grad /(image+1e-8)

        gradient = self._postProcess(grd).sum(1, keepdim=True)

        #cam = gradient
        cam=0
        im_size = image.size()

        # Aggregate Bias-gradients

        for i in range(len(bias_grad)):

            # Select only Conv layers

            if len(bias_grad[i].size()) == len(im_size):
                temp = self._postProcess(bias_grad[i])

                gradient = F.interpolate(temp, size=(im_size[2], im_size[3]), mode='bilinear', align_corners=True)

                cam += gradient.sum(1, keepdim=True)
        for h in self.model_ext.gbp_handles:
            h.remove()
        for h in self.model_ext.grad_handles:
            h.remove()
        return cam
