# -*- coding : utf-8 -*-
# @Time   : 2021/10/3 11:29
# @Author : goodli
# @File   : builder.py
# @Project: Valley 山谷

import enum

from valley.utils.plugin import get_plugin, PluginType
from valley.data.datatype import DataPhase


def build_train_dataloader(cfg):
    model_cls = get_plugin(PluginType.DATALOADER, cfg.DATALOADER.TRAIN)

    return model_cls(cfg, DataPhase.TRAIN)


def build_test_dataloader(cfg):
    model_cls = get_plugin(PluginType.DATALOADER, cfg.DATALOADER.TEST)

    return model_cls(cfg, DataPhase.TEST)
