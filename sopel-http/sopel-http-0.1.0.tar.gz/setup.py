# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sopel_http']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.1.2,<3.0.0', 'gevent>=21.12,<22.0']

entry_points = \
{'sopel.plugins': ['http = sopel_http']}

setup_kwargs = {
    'name': 'sopel-http',
    'version': '0.1.0',
    'description': 'An HTTP server for the Sopel IRC bot framework',
    'long_description': '# sopel-http\n[![PyPi Version](https://img.shields.io/pypi/v/sopel-http.svg)](https://pypi.python.org/pypi/sopel-http)\n\nInteract with your [Sopel](https://github.com/sopel-irc/sopel) bot over HTTP\n\n## Setup\nOnly developers should need to install this package directly, but they can do\nso with a simple `pip install sopel-http`.\n\n## Configuration\nYou can change which IP addresses and ports `sopel-http` binds to in your Sopel\nconfiguration. For example, to bind to port 80 on all IPs (including public!):\n```ini\n[http]\nbind = "[::]:80"\n```\n\n## Usage\nSee the example plugin,\n[sopel-http-example](https://github.com/half-duplex/sopel-http-example).\n\nOnce you\'ve created and registered the flask\n[Blueprint](https://flask.palletsprojects.com/en/2.1.x/blueprints/)\nas shown in the example, you can use it more or less like any other flask\napplication.\n',
    'author': 'Trevor Bergeron',
    'author_email': 'mal@sec.gd',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/half-duplex/sopel-http',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
