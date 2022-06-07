"""Layers for layer-wise relevance propagation.

Layers for layer-wise relevance propagation can be modified.

"""
import torch
from torch import nn
import torch.nn.functional as F

top_k_percent = 0.04  # Proportion of relevance scores that are allowed to pass.


class RelevancePropagationAdaptiveAvgPool2d(nn.Module):
    """Layer-wise relevance propagation for 2D adaptive average pooling.

    Attributes:
        layer: 2D adaptive average pooling layer.
        eps: a value added to the denominator for numerical stability.

    """

    def __init__(self, layer: torch.nn.AdaptiveAvgPool2d, eps: float = 1.0e-05) -> None:
        super().__init__()
        self.layer = layer
        self.eps = eps

    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        z = self.layer.forward(a) + self.eps
        s = (r / z).data
        (z * s).sum().backward()
        c = a.grad
        r = (a * c).data
        return r


class RelevancePropagationAvgPool2d(nn.Module):
    """Layer-wise relevance propagation for 2D average pooling.

    Attributes:
        layer: 2D average pooling layer.
        eps: a value added to the denominator for numerical stability.

    """

    def __init__(self, layer: torch.nn.AvgPool2d, eps: float = 1.0e-05) -> None:
        super().__init__()
        self.layer = layer
        self.eps = eps

    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        z = self.layer.forward(a) + self.eps
        s = (r / z).data
        (z * s).sum().backward()
        c = a.grad
        r = (a * c).data
        return r


class RelevancePropagationMaxPool2d(nn.Module):
    """Layer-wise relevance propagation for 2D max pooling.

    Optionally substitutes max pooling by average pooling layers.

    Attributes:
        layer: 2D max pooling layer.
        eps: a value added to the denominator for numerical stability.

    """

    def __init__(self, layer: torch.nn.MaxPool2d, mode: str = "max", eps: float = 1.0e-05) -> None:
        super().__init__()

        if mode == "avg":
            self.layer = torch.nn.AvgPool2d(kernel_size=(2, 2))
        elif mode == "max":
            self.layer = layer

        self.eps = eps

    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        z = self.layer.forward(a) + self.eps
        s = (r / z).data
        (z * s).sum().backward()
        c = a.grad
        r = (a * c).data
        return r


class RelevancePropagationConv2d(nn.Module):
    """Layer-wise relevance propagation for 2D convolution.

    Optionally modifies layer weights according to propagation rule. Here z^+-rule

    Attributes:
        layer: 2D convolutional layer.
        eps: a value added to the denominator for numerical stability.

    """

    def __init__(self, layer: torch.nn.Conv2d, mode: str = "z_plus", eps: float = 1.0e-05) -> None:
        super().__init__()

        self.layer = layer

        self.stride, self.padding, self.kernel = layer.stride, layer.padding, layer.kernel_size

        self.eps = eps

    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        if a.min()>=0:
            z = F.conv2d(a, F.relu(self.layer.weight), stride=self.stride, padding=self.padding)  + self.eps
            if scale:
                z2 = F.conv2d(a, self.layer.weight, self.layer.bias, stride=self.stride,
                              padding=self.padding)
                z3 = (z2) * torch.sign(F.relu(z2)) + self.eps
                d = (r / z3 * z).data
                scale_value=torch.sum(d.view(r.size(0),-1),1)/torch.sum(r.view(r.size(0),-1),1)
                scale_value=scale_value.view(-1,1,1,1).data
            s = (r / z).data
            (z * s).sum().backward()
            c = a.grad
            r = (a * c).data
            if scale:
                r=r*scale_value
        else:
            print('bottom')
            z0= F.conv2d(-F.relu(-a), -F.relu(-self.layer.weight), stride=self.stride, padding=self.padding) + self.eps
            z1 = F.conv2d(F.relu(a), F.relu(self.layer.weight), stride=self.stride, padding=self.padding) + self.eps
            z=z0+z1
            s = (r / z).data
            (z * s).sum().backward()
            c = a.grad
            r = (a * c).data
        return r



class RelevancePropagationLinear(nn.Module):
    """Layer-wise relevance propagation for linear transformation.

    Optionally modifies layer weights according to propagation rule. Here z^+-rule

    Attributes:
        layer: linear transformation layer.
        eps: a value added to the denominator for numerical stability.

    """

    def __init__(self, layer: torch.nn.Linear, mode: str = "z_plus", eps: float = 1.0e-05) -> None:
        super().__init__()

        self.layer = layer

        self.eps = eps

    @torch.no_grad()
    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        if a.min() >= 0:
            # z+ rule
            z = torch.mm(a, torch.transpose(F.relu(self.layer.weight), 0, 1)) + self.eps
            if scale:
                z2 =  torch.mm(a, torch.transpose(self.layer.weight, 0, 1))+self.layer.bias.view(1, -1)
                if z2.size(1)!=1000 and z2.size(1)!=10:
                    z3 = z2 * torch.sign(F.relu(z2)) + self.eps
                    d = (r / z3 * z).data
                else:
                    d = torch.sign(F.relu(r)) * z2
                scale_value = torch.sum(d.view(r.size(0), -1), 1) / torch.sum(r.view(r.size(0), -1), 1)
                scale_value = scale_value.view(-1, 1).data
                #print(scale_value)
            s = r / z
            c = torch.mm(s, F.relu(self.layer.weight))
            r = (a * c).data
            if scale:
                r=r*scale_value
        else:
            print('new arch')
        return r
class RelevancePropagationFlatten(nn.Module):
    """Layer-wise relevance propagation for flatten operation.

    Attributes:
        layer: flatten layer.

    """

    def __init__(self, layer: torch.nn.Flatten) -> None:
        super().__init__()
        self.layer = layer

    @torch.no_grad()
    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        r = r.view(size=a.shape)
        return r


class RelevancePropagationReLU(nn.Module):
    """Layer-wise relevance propagation for ReLU activation.

    Passes the relevance scores without modification. Might be of use later.

    """

    def __init__(self, layer: torch.nn.ReLU) -> None:
        super().__init__()

    @torch.no_grad()
    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        return r


class RelevancePropagationDropout(nn.Module):
    """Layer-wise relevance propagation for dropout layer.

    Passes the relevance scores without modification. Might be of use later.

    """

    def __init__(self, layer: torch.nn.Dropout) -> None:
        super().__init__()

    @torch.no_grad()
    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        return r


class RelevancePropagationIdentity(nn.Module):
    """Identity layer for relevance propagation.

    Passes relevance scores without modifying them.

    """

    def __init__(self, layer) -> None:
        super().__init__()

    @torch.no_grad()
    def forward(self, a: torch.tensor, r: torch.tensor,scale=False) -> torch.tensor:
        return r
