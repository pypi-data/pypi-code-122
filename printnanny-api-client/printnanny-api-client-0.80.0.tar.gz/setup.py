# coding: utf-8

"""
    printnanny-api-client

    Official API client library forprintnanny.ai print-nanny.com  # noqa: E501

    The version of the OpenAPI document: 0.0.0
    Contact: leigh@printnanny.ai
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_namespace_packages  # noqa: H301

NAME = "printnanny-api-client"
VERSION = "0.80.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.25.3", "six >= 1.10", "python-dateutil", "protobuf"]
REQUIRES.append("aiohttp >= 3.7.0")
setup(
    name=NAME,
    version=VERSION,
    description="printnanny-api-client",
    author="Leigh Johnson",
    author_email="leigh@printnanny.ai",
    url="",
    keywords=["OpenAPI", "OpenAPI-Generator", "printnanny-api-client"],
    install_requires=REQUIRES,
    packages=find_namespace_packages(exclude=["test", "tests"]),
    include_package_data=True,
    license="AGPLv3",
    long_description="""\
    Official API client library forprintnanny.ai print-nanny.com  # noqa: E501
    """
)
