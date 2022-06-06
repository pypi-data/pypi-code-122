# -*- coding: utf-8 -*-

"""Top-level package for zoro_ds_utils."""
import datetime
import pkgutil


__name__ = "zoro_ds_utils"
__version__ = pkgutil.get_data(__name__, "VERSION").decode()  # type: ignore[union-attr]
__author__ = "Zoro Data Science"
__email__ = ""
__copyright__ = f"Copyright (C) {datetime.datetime.now().year} Zoro"
