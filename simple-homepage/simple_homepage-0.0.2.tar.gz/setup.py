# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_homepage']

package_data = \
{'': ['*'],
 'simple_homepage': ['files/*',
                     'files/template/*',
                     'files/template/static/*',
                     'files/template/static/images/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'PyYAML>=6.0,<7.0', 'oyaml>=1.0,<2.0']

entry_points = \
{'console_scripts': ['homepage = simple_homepage.cli:cli']}

setup_kwargs = {
    'name': 'simple-homepage',
    'version': '0.0.2',
    'description': 'Create a simple homepage',
    'long_description': '# simple-homepage\n\n[![Release](https://img.shields.io/github/v/release/fpgmaas/simple-homepage)](https://img.shields.io/github/v/release/fpgmaas/simple-homepage)\n[![Build status](https://img.shields.io/github/workflow/status/fpgmaas/simple-homepage/merge-to-main)](https://img.shields.io/github/workflow/status/fpgmaas/simple-homepage/merge-to-main)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/fpgmaas/simple-homepage)](https://img.shields.io/github/commit-activity/m/fpgmaas/simple-homepage)\n[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://fpgmaas.github.io/simple-homepage/)\n[![Code style with black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports with isort](https://img.shields.io/badge/%20imports-isort-%231674b1)](https://pycqa.github.io/isort/)\n[![License](https://img.shields.io/github/license/fpgmaas/simple-homepage)](https://img.shields.io/github/license/fpgmaas/simple-homepage)\n\nThis repository helps you to create a simple static homepage for your browser.\n\n- **Github repository**: <https://github.com/fpgmaas/simple-homepage/>\n- **Documentation** <https://fpgmaas.github.io/simple-homepage/>\n\n\n\n---\n\nRepository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).',
    'author': 'Florian Maas',
    'author_email': 'ffpgmaas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fpgmaas/simple-homepage',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
