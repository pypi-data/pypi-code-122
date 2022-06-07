"""Flit with extensions"""

import tomli
from flit_core import buildapi  # noqa: F401
from setuptools_scm import get_version

__version__ = "0.0.3"


try:
    with open("pyproject.toml", "rb") as f:
        pyproject = tomli.load(f)
except OSError:
    pass
else:
    try:
        setuptools_scm_config = pyproject["tool"]["setuptools_scm"]
    except KeyError:
        pass
    else:
        get_version(**setuptools_scm_config)
