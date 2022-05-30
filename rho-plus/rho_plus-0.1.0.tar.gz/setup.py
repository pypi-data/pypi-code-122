# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rho_plus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rho-plus',
    'version': '0.1.0',
    'description': 'Aesthetic and ergonomic enhancements to common Python data science tools',
    'long_description': None,
    'author': 'Nicholas Miklaucic',
    'author_email': 'nicholas.miklaucic@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
