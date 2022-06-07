import torch
import torch.nn.functional as F
import torch.nn as nn
from .src.lrp import LRPModel

class Explainer():
    def __init__(self,model,nclass=1000):
        self.model=LRPModel(model)

    def get_attribution_map(self,img,target=None,eval=True):
        if eval:
            self.model.eval()

        temp=self.model.forward(img,target)

        return temp

