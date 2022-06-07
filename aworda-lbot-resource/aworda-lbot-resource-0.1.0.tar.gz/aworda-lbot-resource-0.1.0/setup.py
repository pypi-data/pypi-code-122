# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aworda_lbot_resource']

package_data = \
{'': ['*'],
 'aworda_lbot_resource': ['font/*',
                          'font/nokia/*',
                          'sign-in/*',
                          'sign-in/font/*',
                          'sign-in/hitokoto/cache/*']}

setup_kwargs = {
    'name': 'aworda-lbot-resource',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Little-LinNian',
    'author_email': '2544704967@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
