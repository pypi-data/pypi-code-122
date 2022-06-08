# -*- coding : utf-8 -*-
# @Time   : 2021/10/8 10:46
# @Author : goodli
# @File   : builder.py
# @Project: Valley 山谷

from valley.utils.plugin import get_plugin, PluginType
from valley.data.datatype import DataPhase


def build_dataset(cfg, dataphase):
    if dataphase == DataPhase.TRAIN:
        dataset_cls = get_plugin(PluginType.DATASET, cfg.DATASET.TRAIN.NAME)
    else:
        dataset_cls = get_plugin(PluginType.DATASET, cfg.DATASET.TEST.NAME)

    return dataset_cls(cfg)
