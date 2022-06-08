# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dputils']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'docx2txt>=0.8,<0.9',
 'fake-useragent>=0.1.11,<0.2.0',
 'fpdf2>=2.5.4,<3.0.0',
 'pdfminer.six>=20220524,<20220525',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'dputils',
    'version': '0.1.1',
    'description': 'This library is utility library from digipodium',
    'long_description': None,
    'author': 'AkulS1008',
    'author_email': 'akulsingh0708@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
