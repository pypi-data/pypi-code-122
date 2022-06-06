#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup

import zoro_ds_utils


# Avoid setuptools as an entrypoint unless it's the only way to do it.
# Prefer setup.cfg to setup.py unless not possible.
# Keep setup.py for easy "editable" installs, even if otherwise empty.
setup(
    name=zoro_ds_utils.__name__,
    author=zoro_ds_utils.__author__,
    author_email=zoro_ds_utils.__email__,
)
