# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hereutil']

package_data = \
{'': ['*']}

install_requires = \
['pyprojroot>=0.2.0,<0.3.0']

setup_kwargs = {
    'name': 'hereutil',
    'version': '0.1.0',
    'description': 'Small utility to manage importing/sourcing python from under here()',
    'long_description': '# hereutil\n\nA small set of utility functions to make importing/sourcing python from under here() easier. \n\n',
    'author': 'Eetu Mäkelä',
    'author_email': 'eetu.makela@iki.fi',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hsci-r/hereutil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
