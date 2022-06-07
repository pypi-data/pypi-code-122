# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['growatt_monitor']

package_data = \
{'': ['*']}

install_requires = \
['slugify>=0.0.1,<0.0.2']

entry_points = \
{'console_scripts': ['roundbox-admin = RoundBox.core.cliparser:exec_from_cli']}

setup_kwargs = {
    'name': 'growatt-monitor',
    'version': '1.0.0',
    'description': 'Growatt inverter monitor from Modbus and API server and parse data to different output sources',
    'long_description': "# ⚡ Growatt monitor\n\nGrowatt inverter monitor from Modbus and API server\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI](https://img.shields.io/pypi/v/growatt-monitor?label=GrowattMonitor&style=plastic)\n![GitHub release (latest by date)](https://img.shields.io/github/v/release/soulraven/growatt-monitor?style=plastic)\n[![Build status](https://img.shields.io/github/workflow/status/soulraven/growatt-monitor/merge-to-main?style=plastic)](https://img.shields.io/github/workflow/status/soulraven/growatt-monitor/merge-to-main)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/growatt-monitor?style=plastic)](https://pypi.org/project/growatt-monitor/)\n[![License](https://img.shields.io/github/license/soulraven/growatt-monitor?style=plastic)](https://img.shields.io/github/license/soulraven/growatt-monitor)\n\n***\n\n### 🔧 Installation\n\n### Growatt monitor module\nDownload the repository and use [pip](https://pip.pypa.io/en/stable/) to install Growatt Monitor:\n```bash\ngit clone https://github.com/soulraven/growatt-monitor.git\ncd growatt-monitor\npip install -r requirements.txt .\n```\nTo install for all users on the system, run pip as root:\n```bash\nsudo pip install -r requirements.txt .\n```\n\n***\n\n### Variables\n\nSome variables you may want to set.\n\n`api.server_url` The growatt server URL, default: 'https://server.growatt.com/'\n\n***\n\n### 🌍 Contributions\n\nContributions of all forms are welcome :)\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n***\n\n## 🗒 License\n\nThis project is licensed under [GPLv3].\n\n***\n\n## 👀 Author\n\nZaharia Constantin, my [GitHub profile] and [GitHub Page]\n\n***\n\n[GitHub profile]: https://github.com/soulraven/\n[Github Page]: https://soulraven.github.io/\n[GPLv3]: https://soulraven.github.io/growatt_monitor/license\n",
    'author': 'Zaharia Constantin',
    'author_email': 'layout.webdesign@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/soulraven/growatt-monitor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
