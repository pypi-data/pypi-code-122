# -*- coding : utf-8 -*-
# @Time   : 2021/10/10 9:15
# @Author : goodli
# @File   : datatype.py
# @Project: Valley 山谷

import enum


@enum.unique
class DataPhase(enum.IntEnum):
    TRAIN = 1
    VALID = 2
    TEST  = 3
    ALL   = 10


@enum.unique
class DataType(enum.IntEnum):
    V_RAW_IMAGE     = 0
    V_TARGET_LABEL  = 1
    V_RESULT_LABEL  = 2
    V_EVALUATE_STRING = 3

