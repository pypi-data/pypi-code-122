# -*- coding : utf-8 -*-
# @Time   : 2021/9/30 13:04
# @Author : goodli
# @File   : plugin.py
# @Project: Valley 山谷

import enum
from typing import Dict

@enum.unique
class PluginType(enum.IntEnum):
    ENGINE     = 1
    #MODEL      = 2
    EVALUATOR  = 3
    DATALOADER = 4
    DATASET    = 5
    SOLVER     = 6
    SCHEDULER  = 7
    BACKBONE   = 8
    META_ARCHITECTURE = 9


class PluginRegistry:
    def __init__(self):
        self.plugin_pool: Dict[str:Dict[str:object]] = {}

    def reg(self, plugin_type: PluginType, plugin_name: str, cls):
        #print('reg ' + plugin_name)
        type_plugins = self.plugin_pool.setdefault(plugin_type, {})

        assert(plugin_name not in type_plugins)
        type_plugins[plugin_name] = cls

        #self.plugin_pool.setdefault(plugin_type, type_plugins)

    def get(self, plugin_type: PluginType, plugin_name: str):
        return self.plugin_pool.get(plugin_type, {}).get(plugin_name, None)


_plugin_registry = PluginRegistry()


def reg_plugin(plugin_type: PluginType, plugin_name: str):

    def decorator(cls):
        #print("decorator " + plugin_name)
        _plugin_registry.reg(plugin_type, plugin_name, cls)
        return cls

    return decorator


def get_plugin(plugin_type: PluginType, plugin_name: str):

    return _plugin_registry.get(plugin_type, plugin_name)

