# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hubify']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0']

setup_kwargs = {
    'name': 'hubify',
    'version': '0.1.1',
    'description': 'Create GitHub-like visualisations',
    'long_description': 'hubify\n======\n\nCreate GitHub-like visualisations.\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fferegrino/hubify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
