# -*- coding : utf-8 -*-
# @Time   : 2021/10/1 19:20
# @Author : goodli
# @File   : __init__.py.py
# @Project: Valley 山谷

import enum
from .datatype import DataPhase, DataType
from valley.data.dataloader.builder import build_train_dataloader, build_test_dataloader
#from .dataloader.mnist import mnist
from .dataloader import base
from .dataset.mnist import mnist
#from .dataset.aiac import aiac



