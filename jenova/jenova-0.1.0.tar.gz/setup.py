# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jenova']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'WebOb>=1.8.7,<2.0.0',
 'gunicorn>=20.1.0,<21.0.0',
 'httpx>=0.23.0,<0.24.0',
 'parse>=1.19.0,<2.0.0',
 'requests-wsgi-adapter>=0.4.1,<0.5.0',
 'requests>=2.27.1,<3.0.0',
 'whitenoise>=6.2.0,<7.0.0']

setup_kwargs = {
    'name': 'jenova',
    'version': '0.1.0',
    'description': 'Web framework built for learning purpose',
    'long_description': None,
    'author': 'Tobi-De',
    'author_email': 'tobidegnon@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
