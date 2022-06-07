# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zhinst', 'zhinst.hdiq']

package_data = \
{'': ['*']}

install_requires = \
['ifaddr>=0.1.7,<0.2.0']

setup_kwargs = {
    'name': 'zhinst-hdiq',
    'version': '1.0.1',
    'description': 'API for Zurich Instruments HDIQ devices',
    'long_description': "[![PyPI](https://img.shields.io/pypi/v/zhinst-hdiq.svg)](https://pypi.python.org/pypi/zhinst-hdiq)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n# Zurich Instruments HDIQ (`zhinst-hdiq`)\n\n`zhinst-hdiq` is a package for Python 3.7+ to control a [Zurich Instruments HDIQ IQ Modulator](https://www.zhinst.com/products/hdiq-iq-modulator) via Ethernet connection. Please note that this package is valid only for instruments with serial numbers **14100 and above**.\n\n## Status\nThe `zhinst-hdiq` package is considered stable for general usage. The interface may be subject to incompatible changes between releases, which we will indicate by a change of the major version. Please check the [changelog](#changelog) if you are upgrading.\n\n## Install\nInstall the package with [`pip`](https://packaging.python.org/tutorials/installing-packages/):\n\n```sh\n$ pip install zhinst-hdiq\n```\n\n## Example\nThe example below shows how to connect an HDIQ instrument to a host computer and control operation modes of the HDIQ channels.\n\n```python\nimport zhinst.hdiq.utils\nfrom zhinst.hdiq import Hdiq\n\nhdiq_devices = zhinst.hdiq.utils.discover_devices()\nprint(f'Found devices: {hdiq_devices}')\nhdiq_serial, hdiq_ip = hdiq_devices[0]\nprint(f'Connecting to {hdiq_serial} (IP: {hdiq_ip})')\nhdiq = Hdiq(hdiq_ip)\nchannel = 1                               # HDIQ channel 1; HDIQ has 4 channels: 1, 2, 3, 4\nhdiq.set_rf_to_calib(channel)             # calibration mode in channel 1, set RF to Calib. port\n# hdiq.set_rf_to_exp(channel)             # RF mode in channel 1, set RF to Exp. port\n# hdiq.set_lo_to_exp(channel)             # LO mode in channel 1, set LO to Exp. port\nstatus = hdiq.get_channel_status(channel) # get status of channel 1\nprint(f'channel {channel} -> {status}')\n```\n\n## Contributing\nWe welcome contributions by the community, either as bug reports, fixes and new code. Please use the GitHub issue tracker to report bugs or submit patches. Before developing something new, please get in contact with us.\n\n## License\nThis software is licensed under the terms of the MIT license. See [LICENSE](./LICENSE) for more detail.\n",
    'author': 'Zurich Instruments AG',
    'author_email': 'info@zhinst.com',
    'maintainer': 'Matthias Berg',
    'maintainer_email': 'matthias.berg@zhinst.com',
    'url': 'https://www.zhinst.com/products/hdiq-iq-modulator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
