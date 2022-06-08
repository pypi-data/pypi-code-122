# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hitchcock_roll_flattening']

package_data = \
{'': ['*']}

install_requires = \
['pyroll>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pyroll-hitchcock-roll-flattening',
    'version': '1.0.0',
    'description': 'PyRoll plugin providing the roll flattening model from J. Hitchcock.',
    'long_description': '# PyRoll Roll Flattening\n\nPyRoll plugin providing the roll force correction through flattening by J. Hitchcook adapted by Bohm and Flaxa.\n\nFor the docs, see [here](docs/docs.pdf).\n\nThis project is licensed under the [BSD-3-Clause license](LICENSE).\n\nThe package is available via [PyPi](https://pypi.org/project/pyroll-hitchcook-roll-flattening/) and can be installed with\n    \n    pip install pyroll-hitchcook-roll-flattening\n\n',
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
