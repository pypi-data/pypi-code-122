# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nbnpy']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'nbnpy',
    'version': '0.5.0',
    'description': 'Unofficial NBN API wrapper',
    'long_description': '# NBN-Py\n\n![PyPi Version](https://img.shields.io/pypi/v/nbnpy)\n![Python Versions](https://img.shields.io/pypi/pyversions/nbnpy)\n[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)\n<br/>\n\n[![Code Hygiene](https://github.com/diabolical-ninja/nbnpy/actions/workflows/code_hygiene.yml/badge.svg)](https://github.com/diabolical-ninja/nbnpy/actions/workflows/code_hygiene.yml)\n[![codecov](https://codecov.io/gh/diabolical-ninja/nbn/branch/main/graph/badge.svg?token=hyTE4HlIxK)](https://codecov.io/gh/diabolical-ninja/nbn)\n![black codestyle](https://img.shields.io/badge/Code%20Style-Black-black)\n<br/>\n\n[![Documentation Status](https://readthedocs.org/projects/nbnpy/badge/?version=latest)](https://nbnpy.readthedocs.io/en/latest/?badge=latest)\n\n<br/>\n\nThis package provides an unofficial wrapper of the National Broadband Network\'s (NBN) API. It allows you to programatically lookup address\'s and examine connection details such as the connection type (FTTP, HFC, etc), service type, connection status and more.\n<br/><br/>\n**Disclaimer:** _This project is not affiliated with the NBN._\n\n\n## Installation\n\nInstall `nbnpy` from the Python Package Index:\n\n```console\n$ pip install nbnpy\n```\n\n## Requirements\n\n- Python 3.8+\n\n\n## Usage\n\nThis example gets the LocationID for an address then looks up the NBN connection details for it.\n```python\nimport pprint\nfrom nbnpy.nbn import NBN\n\nnbn_client = NBN()\nlocation_ids = nbn_client.get_location_ids_from_address("1 Flinders Street, Melbourne VIC")\n\n# The "get_location_ids_*" methods return a list of nearby locations\n# For the purpose of this example, the first result will suffice\nlocation_id = location_ids["suggestions"][0]["id"]\n\nlocation_info = nbn_client.location_information(location_id)\npprint.pprint(location_info)\n```\n\n<details>\n  <summary>Location Info Output</summary>\n  \n  ```json\n  {\n        "addressDetail": {\n            "TC2SME": true,\n            "address1": "Unit 1 32 Flinders St",\n            "address2": "Melbourne VIC 3000 Australia",\n            "altReasonCode": "NULL_NA",\n            "cbdpricing": true,\n            "coatChangeReason": "",\n            "disconnectionDate": "Sep 2020",\n            "disconnectionStatus": "PAST",\n            "ee": true,\n            "eec": 1,\n            "formattedAddress": "UNIT 1 32 FLINDERS ST MELBOURNE VIC 3000 Australia",\n            "frustrated": false,\n            "id": "LOC000175010671",\n            "latitude": -37.81540657,\n            "longitude": 144.97344433,\n            "reasonCode": "FTTC_SA",\n            "serviceStatus": "available",\n            "serviceType": "Fixed line",\n            "speedTierAvailability": true,\n            "techFlip": "",\n            "techType": "FTTC",\n            "wp1DisconnectionDate": "11 September 2020",\n            "wp1DisconnectionStatus": "PAST",\n            "wp2DisconnectionDate": "11 September 2020",\n            "wp2DisconnectionStatus": "PAST",\n            "wp3DisconnectionDate": "11 September 2020",\n            "wp3DisconnectionStatus": "PAST",\n            "wp4DisconnectionDate": "11 September 2020",\n            "wp4DisconnectionStatus": "PAST",\n            "zeroBuildCost": true\n        },\n        "servingArea": {\n            "csaId": "CSA300000010316",\n            "description": "Exhibition",\n            "rfsMessage": "Sep 2018",\n            "serviceCategory": "brownfields",\n            "serviceStatus": "available",\n            "serviceType": "Fixed line",\n            "techType": "FTTC"\n        },\n        "timestamp": 1654656817504\n    }  \n  ```\n</details>\n\n\n\n\n## Building the Project\n\nThis package uses `poetry` and `nox` for package management and building. \n\nIf nox is not already installed, install it:\n```console\n$ pip install nox\n```\n\nRun everything including tests and documentation building\n```console\n$ nox\n\n# Or to run a specific stage:\n$ nox -s <stage name>, eg\n$ nox -s tests\n```\n\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue](https://github.com/diabolical-ninja/nbn/issues) along with a detailed description.\n',
    'author': 'Yass',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diabolical-ninja/nbnpy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
