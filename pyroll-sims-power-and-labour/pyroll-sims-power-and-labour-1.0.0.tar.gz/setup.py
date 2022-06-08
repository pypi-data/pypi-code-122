# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sims_power_and_labour']

package_data = \
{'': ['*']}

install_requires = \
['pyroll-hitchcock-roll-flattening>=1.0.0,<2.0.0', 'pyroll>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pyroll-sims-power-and-labour',
    'version': '1.0.0',
    'description': 'Plugin for PyRoll providing the power and labour calculation after R.B. Sims',
    'long_description': '# PyRoll Sims Power and Labour\n\nPlugin for PyRoll providing Power and Labour calculations from R.B. Sims\n\nFor the docs, see [here](docs/docs.pdf).\n\nThis project is licensed under the [BSD-3-Clause license](LICENSE).\n\nThe package is available via [PyPi](https://pypi.org/project/pyroll-sims-power-and-labour/) and can be installed with\n    \n    pip install pyroll-sims-power-and-labour\n\n\n',
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
