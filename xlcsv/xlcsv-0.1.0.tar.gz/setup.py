# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xlcsv']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xlcsv',
    'version': '0.1.0',
    'description': 'A Python micropackage for consuming Excel as CSV.',
    'long_description': None,
    'author': 'Chris Pryer',
    'author_email': 'cnpryer@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
