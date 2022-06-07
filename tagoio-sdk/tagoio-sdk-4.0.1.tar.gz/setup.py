# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tagoio_sdk',
 'tagoio_sdk.common',
 'tagoio_sdk.infrastructure',
 'tagoio_sdk.modules.Account',
 'tagoio_sdk.modules.Analysis',
 'tagoio_sdk.modules.Device',
 'tagoio_sdk.modules.Services',
 'tagoio_sdk.modules.Utils']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.2,<3.0.0',
 'python-socketio[asyncio_client]>=5.6.0,<6.0.0',
 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'tagoio-sdk',
    'version': '4.0.1',
    'description': 'Official Python SDK for TagoIO',
    'long_description': '<br/>\n<p align="center">\n  <img src="https://assets.tago.io/tagoio/sdk.png" width="250px" alt="TODO"></img>\n</p>\n\n# TagoIO - Python SDK\n\nOfficial Python SDK for TagoIO\n\n## Development Commands\n\n```bash\npoetry install\npoetry run pytest tests/\npoetry run flake8 src\n```\n\n## License\n\nTagoIO SDK for Python is released under the [Apache-2.0 License](https://github.com/tago-io/sdk-python/blob/master/LICENSE).\n',
    'author': 'Tago LLC',
    'author_email': 'contact@tago.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tago.io/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
