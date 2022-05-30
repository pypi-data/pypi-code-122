# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fshasher']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fshasher',
    'version': '0.1.0',
    'description': 'Cross-platform file-object hasher',
    'long_description': None,
    'author': 'Matias Grioni',
    'author_email': 'matgrioni@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
