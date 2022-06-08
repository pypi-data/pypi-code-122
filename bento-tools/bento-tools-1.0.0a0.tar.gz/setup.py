# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bento',
 'bento.datasets',
 'bento.io',
 'bento.plotting',
 'bento.preprocessing',
 'bento.tools']

package_data = \
{'': ['*'], 'bento': ['models/*']}

install_requires = \
['Shapely>=1.7.1,<2.0.0',
 'UpSetPlot>=0.6.0,<0.7.0',
 'anndata>=0.7.6,<0.8.0',
 'astropy>=4.3.post1,<5.0',
 'cell2cell>=0.5.10,<0.6.0',
 'dask-geopandas>=0.1.0-alpha.4,<0.2.0',
 'geopandas>=0.9.0,<0.10.0',
 'ipywidgets>=7.6.3,<8.0.0',
 'leidenalg>=0.8.7,<0.9.0',
 'matplotlib-scalebar>=0.8.1,<0.9.0',
 'matplotlib>=3.2,<4.0',
 'numpy>=1.19.0,<2.0.0',
 'pandas<=1.2.5',
 'pygeos>=0.10.1,<0.11.0',
 'scanpy>=1.8.1,<2.0.0',
 'scipy>=1.7.0,<2.0.0',
 'seaborn>=0.11.0,<0.12.0',
 'statsmodels==0.12.2',
 'tqdm>=4.61.2,<5.0.0',
 'umap-learn>=0.5.1,<0.6.0',
 'xgboost>=1.4.0,<1.5']

extras_require = \
{'docs': ['Sphinx>=4.1.2,<5.0.0',
          'sphinx-autobuild>=2021.3.14,<2022.0.0',
          'sphinx-book-theme>=0.3.2,<0.4.0',
          'myst-nb>=0.15.0,<0.16.0'],
 'torch': ['torch>=1.9.0,<2.0.0']}

setup_kwargs = {
    'name': 'bento-tools',
    'version': '1.0.0a0',
    'description': 'A toolkit for subcellular analysis of RNA organization',
    'long_description': '[![PyPI version](https://badge.fury.io/py/bento-tools.svg)](https://badge.fury.io/py/bento-tools)\n[![codecov](https://codecov.io/gh/ckmah/bento-tools/branch/master/graph/badge.svg?token=XVHDKNDCDT)](https://codecov.io/gh/ckmah/bento-tools)\n[![Documentation Status](https://readthedocs.org/projects/bento-tools/badge/?version=latest)](https://bento-tools.readthedocs.io/en/latest/?badge=latest)\n\n# Bento\nBento is a toolkit for ingesting, visualizing, and analyzing spatial transcriptomics data at subcellular resolution. \n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install bento.\n\n```bash\npip install bento-tools\n```\n\n## Usage\n\n```python\nimport bento\n# Todo\n```\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Clarence Mah',
    'author_email': 'ckmah@ucsd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
