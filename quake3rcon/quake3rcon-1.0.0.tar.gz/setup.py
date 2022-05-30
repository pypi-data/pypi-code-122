from setuptools import setup, find_packages

setup(
    name='quake3rcon',
    version='1.0.0',
    url='https://github.com/hellyet/quake3rcon',
    license='MIT',
    author='hellyet',
    author_email='leonid.tosterovski@gmail.com',
    description='A tiny library for using Quake 3\'s RCON protocol feature for some game servers like FiveM.',
    packages=find_packages(exclude=['tests']),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False
)