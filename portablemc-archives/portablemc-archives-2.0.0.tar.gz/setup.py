# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portablemc_archives']

package_data = \
{'': ['*']}

install_requires = \
['portablemc>=3,<4']

setup_kwargs = {
    'name': 'portablemc-archives',
    'version': '2.0.0',
    'description': 'Provides support for archived versions on archive.org manager by Omniarchive community.',
    'long_description': "# Archives add-on\nThe archives addon allows you to install and run old archived versions that are not officially\nlisted by Mojang. It is backed by the [omniarchive](https://omniarchive.net/) work.\n\n![PyPI - Version](https://img.shields.io/pypi/v/portablemc-archives?style=flat-square) &nbsp;![PyPI - Downloads](https://img.shields.io/pypi/dm/portablemc-archives?label=PyPI%20downloads&style=flat-square)\n\n```console\npip install --user portablemc-archives\n```\n\n## Usage\nThis add-on extends the syntax accepted by the [start](/README.md#start-the-game) sub-command, by \nprepending the version with `arc:`. Every version starting with this prefix will be resolved from\narchive repositories hosted on [archives.org](https://archive.org). This addon also add a `-a` \n(`--archives`) flag to the [search](/README.md#search-for-versions) sub-command. You can use it to\nlist all archived versions or search for some specific ones before actually trying to run them.\n\nThe following repositories are used to resolve your versions:\n- [Pre-Classic (Rubydung)](https://archive.org/details/Minecraft-JE-Pre-Classic)\n- [Classic](https://archive.org/details/Minecraft-JE-Classic)\n- [Indev](https://archive.org/details/Minecraft-JE-Indev)\n- [Infdev](https://archive.org/details/Minecraft-JE-Infdev)\n- [Alpha](https://archive.org/details/Minecraft-JE-Alpha)\n- [Beta](https://archive.org/details/Minecraft-JE-Beta)\n\n## Examples\n```sh\nportablemc search -a                # List all archived versions.\nportablemc search -a a1.2.0         # List all archived versions that contains the string 'a1.2.0'.\nportablemc start arc:a1.2.0         # Start the archived version of alpha 1.2.0.\nportablemc start --dry arc:a1.2.0   # Install the archived version of alpha 1.2.0 if it's not already the case.\n```\n\n## Credits\n- [Omniarchive community](https://omniarchive.net/)\n",
    'author': 'Théo Rozier',
    'author_email': 'contact@theorozier.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
