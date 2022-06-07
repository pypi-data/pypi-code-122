# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tnote_plus']

package_data = \
{'': ['*']}

install_requires = \
['getkey>=0.6.5,<0.7.0', 'peewee>=3.14.10,<4.0.0', 'rich>=12.4.4,<13.0.0']

entry_points = \
{'console_scripts': ['tnote = tnote_plus.tnote:main']}

setup_kwargs = {
    'name': 'tnote-plus',
    'version': '0.1.0',
    'description': 'simple CLI notetaking',
    'long_description': "## tnote\n\n[![GitHub license](https://img.shields.io/pypi/l/pyzipcode-cli.svg)](https://img.shields.io/pypi/l/pyzipcode-cli.svg) [![Supported python versions](https://img.shields.io/pypi/pyversions/Django.svg)]([![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]())\n\n```\n             _________ _        _______ _________ _______       _    \n             \\__   __/( (    /|(  ___  )\\__   __/(  ____ \\     ( )   \n                ) (   |  \\  ( || (   ) |   ) (   | (    \\/     | |   \n                | |   |   \\ | || |   | |   | |   | (__       __| |__ \n                | |   | (\\ \\) || |   | |   | |   |  __)     (__   __)\n                | |   | | \\   || |   | |   | |   | (           | |   \n                | |   | )  \\  || (___) |   | |   | (____/\\     | |   \n                )_(   |/    )_)(_______)   )_(   (_______/     (_)   \n                                                                                    \n```\n\nA dead simple command line note taking app built for you! The original project lives here:\nhttps://github.com/tasdikrahman/tnote\n\nAt the time of forking the project, there had been not updates in 4 years with 11 issues. I thought it was interesting\nenough to at least fork it and give it a shot. \n\n## Index\n\n- [Demo](#demo)\n- [Features](#features)\n- [Installation](#installation)\n  - [Installing dependencies](#installing-dependencies)\n  - [Clone it](#clone-it)\n  - [Run it](#run-it)\n- [Supported platforms](#supported-platforms)\n- [Contributing](#contributing)\n  - [To-do](#to-do)\n  - [Contributers](#contributers)\n- [Issues](#issues)\n- [License](#license)\n\n\n## Features\n[:arrow_up: Back to top](#index)\n\n- **Dead simple to use**: Even your granny would be able to use it. No seriously!\n- **Feature rich** Add your precious note with it's _title_ , _content_ , _tags_\n\n**NOTE**\n  _This was built and testing in Linux - use on other OS's at your own risk_\n\n- **Text Highlighting is cross platform** - Supports Linux, Windows, MAC for the terminal based highlighting.\n- **Searching for notes is hassle free** in `tnote`: It supports full text search for notes based on _content_, _tags_\n    - The search query if found in the database will be highlighted if found. Looks pleasing to the eyes\n- Ability to add and remove tags for each note.\n- Adds timestamp for each note which has been added.\n- Written in uncomplicated python.\n\nNeed I say more?\n\n***\n\n## Installation\n[:arrow_up: Back to top](#index)\n\nIf poetry is on the system:\n\n```\npoetry install\n```\n\n\n#### Run it\n\nFire it up! :volcano:\n\n`poetry run ./tnote_plus/tnote.py`\n\n***\n\n\n## Contributing\n[:arrow_up: Back to top](#index)\n\nThis project was originally created in a few hours and utilizes [peewee (ORM)](https://github.com/coleifer/peewee). It\nwas then forked by acherrera to do more work. \n\n### Dependencies\n\nDependencies are managed with [Python Poetry](https://python-poetry.org/). This is also used to publish the package.\n\nInstall poetry with `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -`\n\n### Deployment\n\n`poetry build` will build the project.\n\n`poetry publish` will publish the package to a repository.\n\n#### To-do\n    \n- [x] Convert color handling to Rich\n- [x] Add initial tests\n- [x] Add github actions for tests\n- [ ] Make it pip installable\n- [ ] Ability to edit the content of a note\n- [ ] Add option to remove title for notes\n- [ ] Add option to search for notes using title\n- [ ] Add option to search for notes using timestamp\n- [ ] List titles with number and open based on number\n\n#### Contributers\n\nA big shout out to all the contributers, more specifically to these guys\n\n* OG contributers: \n- [@maxwellgerber](https://github.com/maxwellgerber)\n- [@BrandtM](https://github.com/BrandtM)\n\n## Motivation\n[:arrow_up: Back to top](#index)\n\nOriginal project had not had updates for 4 years, so I thought I would try my hand at understanding what was going on\nand expanding upon the project.\n\n***\n\n## Issues\n[:arrow_up: Back to top](#index)\n\nYou can report the bugs at the [issue tracker](https://github.com/acherrera/tnote_plus/issues)\n\n***\n\n## License\n[:arrow_up: Back to top](#index)\n\nYou can find a copy of the License at http://prodicus.mit-license.org/\n\n",
    'author': 'Anthony Herrera',
    'author_email': 'anthonyherrera24@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/acherrera/tnote_plus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
