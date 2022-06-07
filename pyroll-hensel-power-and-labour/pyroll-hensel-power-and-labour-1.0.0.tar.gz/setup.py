# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hensel_power_and_labour']

package_data = \
{'': ['*']}

install_requires = \
['pyroll>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pyroll-hensel-power-and-labour',
    'version': '1.0.0',
    'description': 'PyRoll plugin providing roll force and roll torque empirical approach by A. Hensel.',
    'long_description': '# PyRoll Hensel Force\n\nPyRoll plugin providing roll force and roll torque empirical approach by A. Hensel',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pyroll-project.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
