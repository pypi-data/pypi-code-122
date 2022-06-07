# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jupyterlab_lsf']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.4,<9.0.0', 'jupyterlab>=3.2.9,<4.0.0']

setup_kwargs = {
    'name': 'jupyterlab-lsf',
    'version': '0.1.0',
    'description': '📙 Run jupyter lab in an LSF host and map its port',
    'long_description': None,
    'author': 'Juanes',
    'author_email': 'juanes.ao@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
