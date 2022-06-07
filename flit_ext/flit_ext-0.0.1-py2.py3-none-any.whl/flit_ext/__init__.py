"""Flit with extensions"""

import tomli
from flit_core import buildapi  # noqa: F401
from setuptools_scm import ScmVersion, get_version

__version__ = "0.0.1"


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


def local_version(version: ScmVersion):
    return version.format_choice("+{node}", "+{node}.d{time:%Y%m%d}")
