# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hill_spreading']

package_data = \
{'': ['*']}

install_requires = \
['pyroll>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pyroll-hill-spreading',
    'version': '1.0.0',
    'description': 'Plugin for PyRoll providing the Hill spreading model.',
    'long_description': '# PyRoll Hill Spreading\n\nPlugin for PyRoll providing the Hill spreading model.\n\nFor the docs, see [here](docs/docs.pdf).\n\nThis project is licensed under the [BSD-3-Clause license](LICENSE).\n\nThe package is available via [PyPi](https://pypi.org/project/pyroll-hill-spreading/) and can be installed with\n    \n    pip install pyroll-hill-spreading',
    'author': 'Christoph Renzing',
    'author_email': 'christoph.renzing@imf.tu-freiberg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pyroll-project.github.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
