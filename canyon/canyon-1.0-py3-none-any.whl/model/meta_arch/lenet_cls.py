
import torch
import torch.nn as nn
import torch.nn.functional as F

from valley.utils.plugin import reg_plugin, PluginType
from valley.config import configurable
from valley.utils import comm

from ..backbone import Backbone, build_backbone

@reg_plugin(PluginType.META_ARCHITECTURE, 'LeNet_CLS')
class LeNetCLS(nn.Module):

    @configurable
    def __init__(self, *, backbone: Backbone):
        super().__init__()
        self.backbone = backbone
        
        self.fc1 = nn.Linear(9216, 128)
        self.fc2 = nn.Linear(128, 10)
        self.dropout2 = nn.Dropout2d(0.5)
        self.batchnorm = nn.SyncBatchNorm(128)

        self.cal_loss = nn.NLLLoss()

    @classmethod
    def from_config(cls, cfg):
        backbone = build_backbone(cfg)

        return {
            "backbone": backbone,
        }

    def _forward(self, x):
        x = self.backbone(x) 

        x = self.fc1(x)
        x = self.batchnorm(x)
        x = F.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)

        predict = F.log_softmax(x, dim=1)

        return predict

    def forward(self, x):
        image = x["image"].to("cuda")
        label = x["label"].to("cuda")

        predict = self._forward(image)

        if self.training:
            return {"loss": self.cal_loss(predict, label)}
        else:
            return {"predict": predict}



