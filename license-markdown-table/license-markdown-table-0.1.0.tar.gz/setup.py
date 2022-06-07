# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['license_markdown_table']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.11.4,<5.0.0',
 'pandas>=1.4.2,<2.0.0',
 'prettytable>=3.3.0,<4.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'toml>=0.10.2,<0.11.0',
 'wheel>=0.37.1,<0.38.0']

setup_kwargs = {
    'name': 'license-markdown-table',
    'version': '0.1.0',
    'description': 'Gathers project dependencies and creates a markdown table with license information for each package.',
    'long_description': '[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)',
    'author': 'szmyty',
    'author_email': 'szmyty@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/szmyty/license-markdown-table',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
