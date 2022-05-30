# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['travel_map', 'travel_map.scripts']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'pyecharts>=1.9.1,<2.0.0']

extras_require = \
{'test': ['pytest>=7.1.2,<8.0.0', 'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['travel-map = travel_map.scripts.commands:travel_map']}

setup_kwargs = {
    'name': 'travel-map',
    'version': '2.0.1',
    'description': 'A tool to generate travel map.',
    'long_description': '# 旅行地图\n\n这是一个精确到城市旅行地图生成器。\n本项目是基于开源项目 [pyechart](https://github.com/pyecharts/pyecharts)，\n生成的中国地图符合法律规范。\n\n[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/hktkzyx/travel-map/Build%20and%20Test%20Python%20Package)](https://github.com/hktkzyx/travel-map/actions/workflows/build_and_test.yml)\n[![Codecov](https://img.shields.io/codecov/c/github/hktkzyx/travel-map)](https://app.codecov.io/gh/hktkzyx/travel-map)\n[![PyPI](https://img.shields.io/pypi/v/travel-map)](https://pypi.org/project/travel-map/)\n[![PyPI - License](https://img.shields.io/pypi/l/travel-map)](https://github.com/hktkzyx/travel-map/blob/main/LICENSE)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/travel-map)](https://img.shields.io/pypi/pyversions/travel-map)\n[![GitHub last commit](https://img.shields.io/github/last-commit/hktkzyx/travel-map)](https://github.com/hktkzyx/travel-map/commits/main)\n\n## 安装\n\n```bash\npip install travel-map\n```\n\n## 使用\n\n用户需要将旅行信息输入到一个 CSV 文件里，例如\n\n```csv travelled_cities.csv\n城市,组\n北京,旅行\n上海,旅行\n武汉,居住\n香港,中转\n```\n\n文件中城市的名称可以查阅[文件](https://github.com/pyecharts/pyecharts/blob/d1b2ecd223b6c6d429e698ec690e15bf8c40ae09/pyecharts/datasets/map_filename.json)。\n\n然后运行命令\n\n```bash\ntravel-map --title "我的旅行地图" --output travel_map.html travelled_cities.csv\n```\n\n即可生成标题为`我的旅行地图`的精确到城市的旅行地图如下\n\n![demo](./demo/demo.png)\n\n## 贡献\n\n如果你想提交你的代码，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。\n\n## 许可证\n\n木兰宽松许可证，第2版 （Mulan Permissive Software License，Version 2）\n\nCopyright (c) 2019 Brooks YUAN\n\ntravel-map is licensed under Mulan PSL v2.\n\nYou can use this software according to the terms and conditions of the Mulan PSL v2.\n\nYou may obtain a copy of Mulan PSL v2 at: <http://license.coscl.org.cn/MulanPSL2>\n\nTHIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,\nEITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,\nMERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.\n\nSee the Mulan PSL v2 for more details.\n',
    'author': 'Brooks YUAN',
    'author_email': 'hktkzyx@yeah.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hktkzyx/travel-map',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
