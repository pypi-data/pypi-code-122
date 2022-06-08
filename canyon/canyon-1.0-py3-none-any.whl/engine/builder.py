# -*- coding : utf-8 -*-
# @Time   : 2021/10/1 16:33
# @Author : goodli
# @File   : builder.py
# @Project: Valley 山谷

from valley.utils import plugin


def build(cfg):
    model_cls = plugin.get_plugin(plugin.PluginType.ENGINE, cfg.ENGINE.NAME)

    return model_cls(cfg)
