# -*- coding : utf-8 -*-
# @Time   : 2021/10/1 21:47
# @Author : goodli
# @File   : lenet.py
# @Project: Valley 山谷

import torch
import torch.nn as nn
import torch.nn.functional as F

from valley.utils.plugin import reg_plugin, PluginType
from valley.config import configurable
from valley.data import DataType
from valley.utils import comm
from valley.model.backbone import Backbone

class LeNet(Backbone):
    def __init__(self):
        super(LeNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, 3, 1)
        self.conv2 = nn.Conv2d(32, 64, 3, 1)
        self.dropout1 = nn.Dropout2d(0.25)

    def forward(self, x):
        x = self.conv1(x)
        x = F.relu(x)
        x = self.conv2(x)
        x = F.relu(x)
        x = F.max_pool2d(x, 2)
        x = self.dropout1(x)
        x = torch.flatten(x, 1)
        return x

@reg_plugin(PluginType.BACKBONE, "build_lenet_backbone")
def build_lenet_backbone(cfg, input_shape):
    return LeNet()