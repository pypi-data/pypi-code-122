# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['net_inspect', 'net_inspect.plugins']

package_data = \
{'': ['*']}

install_requires = \
['ntc_templates_elinpf>=3.1.0,<4.0.0',
 'python-Levenshtein-wheels>=0.13.2,<0.14.0',
 'rich>=12.4.1,<13.0.0',
 'textfsm>=1.1.2,<2.0.0',
 'thefuzz>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'net-inspect',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Elin',
    'author_email': '365433079@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
