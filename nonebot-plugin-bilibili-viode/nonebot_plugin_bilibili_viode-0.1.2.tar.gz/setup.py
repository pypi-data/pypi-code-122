# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_bilibili_viode']

package_data = \
{'': ['*'],
 'nonebot_plugin_bilibili_viode': ['resource/font/*', 'resource/image/*']}

install_requires = \
['Pillow>=9.1.1,<10.0.0',
 'httpx>=0.22.0,<0.23.0',
 'nonebot-plugin-guild-patch>=0.1.3,<0.2.0',
 'qrcode[pil]>=7.3.1,<8.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-bilibili-viode',
    'version': '0.1.2',
    'description': '一个nonebot2插件，用于获取哔哩哔哩伪分享卡片',
    'long_description': '# nonebot_plugin_bilibili_viode\n\nnonebot_plugin_bilibili_viode是一个Nonebot2的插件，其功能为将用户发送的B站视频ID转为(伪)分享卡片的形式  \n\n## 如何安装使用\n### 安装\n`pip install nonebot_plugin_bilibili_viode`  \n或者  \n`poetry add nonebot_plugin_bilibili_viode`  \n### 升级  \n`pip install -U nonebot_plugin_bilibili_viode`  \n或者  \n`poetry add nonebot_plugin_bilibili_viode@latest`  \n### 使用\n在你的nontbot项目中的bot.py文件中添加  \n`nonebot.load_plugin("nonebot_plugin_bilibili_viode")`\n### Nonebot配置项\n|配置键名|默认值|作用|  \n|-|-|-|  \n|`bilibili_poster`|True|是否使用海报分享图片样式|  \n## 许可\nMIT\n',
    'author': 'ASTWY',
    'author_email': 'astwy@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/nonebot_plugin_bilibili_viode/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
