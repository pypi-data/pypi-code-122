from setuptools import setup

setup(
    name='yandex_translate_api',
    version='1.1',
    description='Перевод текст через API Yandex',
    packages=['yandex_translate_api'],
    author_email='cklfgads@knowledgemd.com',
    install_requires=['requests', 'aiohttp']
)