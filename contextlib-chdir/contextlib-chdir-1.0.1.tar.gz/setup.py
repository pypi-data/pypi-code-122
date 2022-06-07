# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['contextlib_chdir']
setup_kwargs = {
    'name': 'contextlib-chdir',
    'version': '1.0.1',
    'description': 'Backport of contextlib.chdir stdlib class added in Python3.11.',
    'long_description': "# contextlib-chdir\n\nBackport of [`contextlib.chdir`] stdlib class added in Python3.11.\n\n## Install\n\n```\npip install contextlib-chdir\n```\n\n## Usage\n\n```python\nimport os\nimport tempfile\nfrom contextlib_chdir import chdir as chdir_ctx\n\nwith chdir_ctx(tempfile.gettempdir()):\n    print(os.getcwd())  # /tmp\n```\n\n## Note\n\nYou'll probably want to migrate to [`contextlib2`] when\n[this change is included](https://github.com/jazzband/contextlib2/issues/43).\n\n[`contextlib.chdir`]: https://docs.python.org/3.11/library/contextlib.html#contextlib.chdir\n[`contextlib2`]: https://github.com/jazzband/contextlib2\n",
    'author': 'Álvaro Mondéjar Rubio',
    'author_email': 'mondejar1994@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
