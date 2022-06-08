# -*- coding : utf-8 -*-
# @Time   : 2021/10/27 12:11
# @Author : goodli
# @File   : file_io.py
# @Project: Valley 山谷

from iopath.common.file_io import HTTPURLHandler, OneDrivePathHandler, PathHandler
from iopath.common.file_io import PathManager as PathManagerBase

__all__ = ["PathManager", "PathHandler"]


PathManager = PathManagerBase()

PathManager.register_handler(HTTPURLHandler())
PathManager.register_handler(OneDrivePathHandler())