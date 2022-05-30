# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_sirene', 'tap_sirene.tests']

package_data = \
{'': ['*'], 'tap_sirene': ['schemas/*']}

install_requires = \
['requests>=2.25.1,<3.0.0', 'singer-sdk>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['tap-sirene = tap_sirene.tap:TapSIRENE.cli']}

setup_kwargs = {
    'name': 'tap-sirene',
    'version': '0.0.1',
    'description': '`tap-sirene` is a Singer tap for SIRENE, built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Ilkka Peltola',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
