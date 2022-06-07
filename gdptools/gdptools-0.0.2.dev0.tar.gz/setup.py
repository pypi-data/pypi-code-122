# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gdptools', 'gdptools.process']

package_data = \
{'': ['*']}

install_requires = \
['Bottleneck>=1.3.4,<2.0.0',
 'MetPy>=1.3.0,<2.0.0',
 'Pydap>=3.2.2,<4.0.0',
 'Shapely>=1.8.1,<2.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'awscliv2>=2.2.0,<3.0.0',
 'cftime>=1.6.0,<2.0.0',
 'click<8',
 'dask>=2022.4.0,<2023.0.0',
 'distributed>=2022.4.1,<2023.0.0',
 'geopandas>=0.10.2,<0.11.0',
 'intake>=0.6.5,<0.7.0',
 'netCDF4>=1.5.8,<2.0.0',
 'numpy<=1.21',
 'pandas>=1.4.2,<2.0.0',
 'pygeoapi>=0.11.0,<0.12.0',
 'pygeos>=0.12.0,<0.13.0',
 'pyproj>=3.3.0,<4.0.0',
 'pystac>=1.4.0,<2.0.0',
 'rasterio>=1.2.10,<2.0.0',
 'rasterstats>=0.16.0,<0.17.0',
 'requests>=2.27.1,<3.0.0',
 's3fs>=2022.3.0,<2023.0.0',
 'scipy>=1.8.0,<2.0.0',
 'siphon>=0.9,<0.10',
 'xarray<2022.3.0',
 'zarr>=2.11.1,<3.0.0']

entry_points = \
{'console_scripts': ['gdptools = gdptools.__main__:main']}

setup_kwargs = {
    'name': 'gdptools',
    'version': '0.0.2.dev0',
    'description': 'Gdptools',
    'long_description': "---\ntitle: README\n---Gdptools\n========\n\n[![PyPI](https://img.shields.io/pypi/v/gdptools.svg)](https://pypi.org/project/gdptools/)\n[![Status](https://img.shields.io/pypi/status/gdptools.svg)](https://pypi.org/project/gdptools/)\n[![Python Version](https://img.shields.io/pypi/pyversions/gdptools)](https://pypi.org/project/gdptools)\n[![License](https://img.shields.io/pypi/l/gdptools)](https://creativecommons.org/publicdomain/zero/1.0/legalcode)\n\n[![Read the documentation at https://gdptools.readthedocs.io/](https://img.shields.io/readthedocs/gdptools/latest.svg?label=Read%20the%20Docs)](https://gdptools.readthedocs.io/)\n[![Tests](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/workflows/Tests/badge.svg)](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/wma/nhgf/toolsteam/gdptools/branch/main/graph/badge.svg)](https://codecov.io/gh/wma/nhgf/toolsteam/gdptools)\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://code.usgs.gov/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://code.usgs.gov/psf/black)\n[![Poetry](https://img.shields.io/badge/poetry-enabled-blue)](https://python-poetry.org/)\n[![Conda](https://img.shields.io/badge/conda-enabled-green)](https://anaconda.org/)\n\nFeatures\n========\n\n-   TODO\n\nRequirements\n============\n\n-   TODO\n\nInstallation\n============\n\nYou can install *Gdptools* via [pip](https://pip.pypa.io/) from [PyPI](https://pypi.org/):\n\n        pip install gdptools\n\nUsage\n=====\n\nPlease see the [Command-line Reference](Usage_) for details.\n\nContributing\n============\n\nContributions are very welcome. To learn more, see the Contributor Guide\\_.\n\nLicense\n=======\n\nDistributed under the terms of the [CC0 1.0 Universal license](https://creativecommons.org/publicdomain/zero/1.0/legalcode), *Gdptools* is free and open source software.\n\nIssues\n======\n\nIf you encounter any problems, please [file an issue](https://code.usgs.gov/wma/nhgf/toolsteam/gdptools/issues) along with a detailed description.\n\nCredits\n=======\n\nThis project was generated from [@hillc-usgs](https://code.usgs.gov/hillc-usgs)'s [Pygeoapi Plugin Cookiecutter](https://code.usgs.gov/wma/nhgf/pygeoapi-plugin-cookiecutter) template.\n",
    'author': 'Richard McDonald',
    'author_email': 'rmcd@usgs.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://code.usgs.gov/wma/nhgf/toolsteam/gdptools',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
