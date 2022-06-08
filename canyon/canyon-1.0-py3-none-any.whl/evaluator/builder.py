# -*- coding : utf-8 -*-
# @Time   : 2021/10/10 17:33
# @Author : goodli
# @File   : builder.py
# @Project: Valley 山谷

from valley.utils.plugin import get_plugin, PluginType


def build_evaluator(cfg):
    model_cls = get_plugin(PluginType.EVALUATOR, cfg.EVALUATOR.NAME)

    return model_cls(cfg)