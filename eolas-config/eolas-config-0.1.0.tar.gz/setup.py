# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eolas_config']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'eolas-config',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'James Dooley',
    'author_email': '81564302+dooley-ch@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
