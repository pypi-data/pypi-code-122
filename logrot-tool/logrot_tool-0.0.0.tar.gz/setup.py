#!/usr/bin/env python3


from setuptools import setup


try:
    from logrot import __version__
except ImportError:
    __version__ = "unknown"


setup(
    name="logrot_tool",
    version=__version__,
    description="Log rotation tool in Python",
    author="Maciej Barć",
    author_email="xgqt@riseup.net",
    url="https://gitlab.com/xgqt/python-logrot",
    license="GPL-3",
    keywords="system",
    python_requires=">=3.6.*",
    install_requires=[],
    packages=["logrot"],
    include_package_data=True,
    zip_safe=False,
    entry_points={"console_scripts": ["logrot = logrot.main:main"]},
)
