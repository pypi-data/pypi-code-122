from captum.attr import IntegratedGradients

import torch
import numpy as np
import torch.nn.functional as F

class Explainer():
    def __init__(self,model,nclass=1000):
        self.model=model
        self.model.eval()

    def get_gradient(self,x,target):
        x.requires_grad_(True)
        out=self.model(x)
        iii = torch.LongTensor(range(x.size(0))).cuda()
        grad=torch.autograd.grad(torch.sum(out[iii,target]),x)[0]
        return grad

    def get_attribution_map(self,img,target=None):
        if target is None:
            target=torch.argmax(self.model(img),1)
        baseline = torch.randn_like(img) * 0.001
        mask0=torch.zeros_like(baseline)
        attributions=torch.zeros_like(img)
        grad=self.get_gradient(baseline,target)
        p=10
        while p<=100:
            grad=grad*(1-mask0)
            temp = np.percentile(torch.abs(grad).view(grad.size(0), -1).data.cpu().numpy(), p, axis=1)
            temp = torch.Tensor(temp).cuda().view(grad.size(0), 1, 1, 1)
            mask1=torch.le(torch.abs(grad), temp).float()
            x=img*mask1+baseline*(1-mask1)
            grad=self.get_gradient(x,target)
            p+=10
            attributions+=grad*(img-baseline)*(mask1-mask0)
            mask0=mask1
        #return torch.abs(attributions)
        return attributions