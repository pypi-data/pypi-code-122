# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adfpy', 'adfpy.activities']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1.7.1,<2.0.0', 'azure-mgmt-datafactory>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['adfpy-deploy = adfpy.deploy:run_deployment']}

setup_kwargs = {
    'name': 'adfpy',
    'version': '0.0.2',
    'description': 'A Pythonic wrapper for Azure Data Factory',
    'long_description': "# adfPy\nadfPy aims to make developers lives easier by wrapping the Azure Data Factory Python SDK with an intuitive, powerful, and easy to use API that hopefully will remind people of working with Apache Airflow ;-). \n\n## Install\n```shell\npip install adfpy\n```\n\n## Usage\nGenerally, using adfPy has 2 main components:\n1. Write your pipeline.\n2. Deploy your pipeline.\n\nadfPy has an opinionated syntax, which is heavily influenced by Airflow. For documentation on what the syntax looks like, please read the docs [here]().\nSome examples are provided in the examples directory of this repository.\n\n\nOnce you've written your pipelines, it's time to deploy them! For this, you can use adfPy's deployment script:\n```shell\npip install adfpy\nadfpy-deploy\n```\nNote:\n- This script will ensure all pipelines in the provided path are present in your target ADF.\n- This script will also **remove** any ADF pipelines that are **not** in your path, but are in ADF.\n\n## Still to come\nadfPy is still in development. As such, some ADF components are not yet supported:\n- datasets\n- linked services\n- triggers\n\n## Developer setup\nadfPy is built with [Poetry](https://python-poetry.org/). To setup a development environment run:\n```shell\npoetry install\n```\n",
    'author': 'Daniel van der Ende',
    'author_email': 'daniel.vanderende@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielvdende/adfpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
