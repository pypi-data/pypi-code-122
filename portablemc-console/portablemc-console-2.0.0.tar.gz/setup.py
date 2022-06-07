# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portablemc_console']

package_data = \
{'': ['*']}

install_requires = \
['portablemc>=3,<4', 'prompt-toolkit>=3.0.16,<3.1.0']

setup_kwargs = {
    'name': 'portablemc-console',
    'version': '2.0.0',
    'description': "Provide an interactive console for the Minecraft process' output. Also provide an API for other addons to customize the UI.",
    'long_description': "# Console add-on\nThis addon provides an interactive console for Minecraft process' output. this is useful to debug \nthe game when it crashes multiple times, or simply if you can to track what's going on.\n\n![PyPI - Version](https://img.shields.io/pypi/v/portablemc-console?style=flat-square) &nbsp;![PyPI - Downloads](https://img.shields.io/pypi/dm/portablemc-console?label=PyPI%20downloads&style=flat-square)\n\n```console\npip install --user portablemc-console\n```\n\n## Usage\n**This addon requires you to install the [prompt_toolkit](https://pypi.org/project/prompt-toolkit/) python \nlibrary.**\n\nThis addon is enabled by default when launching the game with the `start` sub-command. To disable \nit and fall back to the default process' output, you can add the `--no-console` flag to the command\nline. By default, when the game ends, you need to do Ctrl+C again to close the terminal, you\ncan disable it using the `--single-exit` flag in the command, this will cause your interactive\nconsole to close with the game's process.\n\n## Examples\n```sh\nportablemc start my_version               # Starts the game and open the interactive console. \nportablemc start --no-console my_version  # Starts the game and don't open the interactive console.\n```\n\n![interactive console screenshot](/doc/assets/console.png)\n\n## Credits\n- [PyPI page of prompt_toolkit](https://pypi.org/project/prompt-toolkit/)\n",
    'author': 'Théo Rozier',
    'author_email': 'contact@theorozier.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2',
}


setup(**setup_kwargs)
