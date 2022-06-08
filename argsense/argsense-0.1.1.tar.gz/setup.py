# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['argsense',
 'argsense.click_vendor',
 'argsense.parser',
 'argsense.style',
 'argsense.style.color_scheme']

package_data = \
{'': ['*']}

install_requires = \
['rich']

setup_kwargs = {
    'name': 'argsense',
    'version': '0.1.1',
    'description': 'New command line interface based on Python Rich library.',
    'long_description': '# Argsense CLI\n\n> The documentation is under construction.\n\n![](.assets/gQqE28Z6lC.png "(outdated)")\n\n![](.assets/20220606164759.jpg "latest")\n\n**argsense** is a command line interface made with Python.\n\n## Usage\n\n```python\nfrom argsense import cli\n\n@cli.cmd\ndef hello(name: str):\n    print(f\'Hello {name}!\')\n\nif __name__ == \'__main__\':\n    cli.run()\n```\n',
    'author': 'Likianta',
    'author_email': 'likianta@foxmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/likianta/argsense-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
