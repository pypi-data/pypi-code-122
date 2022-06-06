"""
Copyright (c) 2022 Ben

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
from setuptools import setup
import os.path


def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, "rb") as f:
            return f.read().decode("utf8")
    except IOError:
        pass


def get_readme():
    return get_file(os.path.dirname(__file__), "README.md")


def get_version():
    version = "0.0.1"
    return version


def get_requirements():
    requirements = ["httpx<=0.23.0", "setuptools==58.1.0", "aiohttp<=3.8.1"]
    return requirements


setup(
    name="aiojikan",
    version="0.0.1",
    author="Ben Zhou",
    author_email="bleg3ndary@gmail.com",
    description=("A up to date asynchronous api wrapper for the jikan api"),
    license="MIT",
    keywords="api jikan wrapper",
    url="http://github.com/Leg3ndary/aiojikan",
    packages=["aiojikan"],
    long_description=get_readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Framework :: aiohttp",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Topic :: Utilities",
    ],
)
