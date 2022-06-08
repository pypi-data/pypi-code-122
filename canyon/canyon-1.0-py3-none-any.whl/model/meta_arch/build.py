import torch
from valley.utils.plugin import get_plugin, PluginType

def build_model(cfg):
    
    meta_arch = cfg.MODEL.META_ARCHITECTURE

    model_cls = get_plugin(PluginType.META_ARCHITECTURE, meta_arch)

    model = model_cls(cfg)

    model.to(torch.device(cfg.MODEL.DEVICE))

    return model

    