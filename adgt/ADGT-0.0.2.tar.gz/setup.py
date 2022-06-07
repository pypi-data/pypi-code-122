#!/usr/bin/env python3
#coding=utf8

# Welcome to the PyTorch ADGT setup.py.
#
#

import os
import re
import subprocess
import sys

from setuptools import find_packages, setup

REQUIRED_MAJOR = 3
REQUIRED_MINOR = 6

# Check for python version
if sys.version_info < (REQUIRED_MAJOR, REQUIRED_MINOR):
    error = (
        "Your version of python ({major}.{minor}) is too old. You need "
        "python >= {required_major}.{required_minor}."
    ).format(
        major=sys.version_info.major,
        minor=sys.version_info.minor,
        required_minor=REQUIRED_MINOR,
        required_major=REQUIRED_MAJOR,
    )
    sys.exit(error)


# Allow for environment variable checks
def check_env_flag(name, default=""):
    return os.getenv(name, default).upper() in ["ON", "1", "YES", "TRUE", "Y"]


VERBOSE_SCRIPT = True
for arg in sys.argv:
    if arg == "-q" or arg == "--quiet":
        VERBOSE_SCRIPT = False


def report(*args):
    if VERBOSE_SCRIPT:
        print(*args)
    else:
        pass


# get version string from module
with open(os.path.join(os.path.dirname(__file__), "__init__.py"), "r") as f:
    version = re.search(r"__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M).group(1)
    report("-- Building version " + version)

# read in README.md as the long description
with open("README.md", "r") as fh:
    long_description = fh.read()


if __name__ == "__main__":

    setup(
        name="ADGT",
        version=version,
        description="Model interpretability for PyTorch",
        author="Guanhua Zheng",
        license="BSD-3",
        url="https://github.com/iceshade000/ADGT",
        project_urls={
            "Documentation": "https://github.com/iceshade000/ADGT",
            "Source": "https://github.com/iceshade000/ADGT",
            "conda": "https://github.com/iceshade000/ADGT",
        },
        keywords=[
            "Model Interpretability",
            "Model Understanding",
            "Feature Importance",
            "PyTorch",
        ],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Scientific/Engineering",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        python_requires=">=3.6",
        install_requires=["matplotlib", "numpy", "torch>=1.6", "captum"],
        packages=find_packages(exclude=("demo")),
    )