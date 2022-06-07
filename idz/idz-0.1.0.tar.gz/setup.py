# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['idz']

package_data = \
{'': ['*']}

install_requires = \
['opencv-contrib-python>=4.5.5,<5.0.0', 'opencv-python>=4.5.5,<5.0.0']

setup_kwargs = {
    'name': 'idz',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'k4w411p0wer',
    'author_email': 'alexandrvasyutin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.11',
}


setup(**setup_kwargs)
