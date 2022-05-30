# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sopel_http_example']

package_data = \
{'': ['*'], 'sopel_http_example': ['static/*', 'templates/*']}

install_requires = \
['Flask>=2.1.2,<3.0.0', 'sopel-http>=0.1.0,<0.2.0', 'sopel>=7.1.9,<8.0.0']

entry_points = \
{'sopel.plugins': ['http-example = sopel_http_example']}

setup_kwargs = {
    'name': 'sopel-http-example',
    'version': '0.1.0',
    'description': 'An example Sopel plugin making use of sopel-http',
    'long_description': '# sopel-http-example\n[![PyPi Version](https://img.shields.io/pypi/v/sopel-http-example.svg)](https://pypi.org/project/sopel-http-example/)\n\nAn example plugin for [sopel-http](https://github.com/half-duplex/sopel-http)\n\n## Setup\nJust `pip install sopel-http-example` into your\n[Sopel](https://github.com/sopel-irc/sopel) environment.\n\n## Usage\nOnce this plugin is installed and your bot is restarted, you should be able to\naccess the web UI on https://localhost:8094/ (or whatever host/port you\nconfigured `sopel-http` to use).\n',
    'author': 'Trevor Bergeron',
    'author_email': 'mal@sec.gd',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/half-duplex/sopel-http-example',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
