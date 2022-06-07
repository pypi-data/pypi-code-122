"""jupyterlab-lsf setup.py."""

from os.path import abspath
from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup

ROOT = abspath(dirname(__file__))

# See 4 > https://packaging.python.org/guides/single-sourcing-package-version/
with open(join(ROOT, "jupyterlab_lsf", "VERSION"), "r") as f:
    VERSION = f.read().strip()

setup(
    name="jupyterlab-lsf",
    description="📙 Run jupyter lab in an LSF host and map its port",
    long_description="📙 Run jupyter lab in an LSF host and map its port. Learn more in [GitHub](https://github.com/juanesarango/jupyterlab-lsf)!",
    long_description_content_type="text/markdown",
    # single source package version
    version=VERSION,
    # in combination with recursive-includes in MANIFEST.in, non-python files
    # within the toil_mutect will be copied into the
    # site-packages and wheels installation directories
    include_package_data=True,
    # return a list all Python packages found within the ROOT directory
    packages=find_packages(),
    # pass parameters loaded from setup.json including author and version
    author="Juan E. Arango <juanes.ao@gmail.com>",
    url="https://github.com/juanesarango/jupyterlab-lsf",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities"
    ],
    entry_points={
        "console_scripts": [
            "jupyterlab-lsf=jupyterlab_lsf.main:submit_notebook_to_lsf"
        ]
    },
    setup_requires=[
        "pytest-runner>=5.3.1"
    ],
    install_requires=[
        "click>=8.0.0",
        "jupyterlab>=3.2.9"
    ],
    extras_require={
        "test": [
            "black>=22.3.0",
            "coverage>=5.5",
            "pydocstyle>=6.1.1",
            "pytest-cov>=2.12.1",
            "pytest-env==0.6.2",
            "pylint>=2.10.2",
            "tox==2.9.1",
        ]
    },
    keywords=["jupyterlab", "lsf"],
    license="BSD",
    test_suite="tests",
    python_requires='>=3.6',
    py_modules=["@papaemmelab/jupyterlab-lsf"],
)
