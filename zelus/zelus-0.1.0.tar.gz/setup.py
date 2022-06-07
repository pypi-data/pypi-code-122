# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zelus',
 'zelus.src',
 'zelus.src.infrastructures',
 'zelus.src.infrastructures.twitter',
 'zelus.src.repositories',
 'zelus.src.repositories.twitter',
 'zelus.src.services',
 'zelus.src.services.twitter']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0', 'TwitterAPI>=2.7.11,<3.0.0', 'tweepy>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'zelus',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'João Pedro Jacques Hoss',
    'author_email': 'joaopedro_jh@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
