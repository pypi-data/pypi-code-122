"""
Quart-Discord
-------------

An Discord OAuth2 quart extension using modern .
"""

import re
import os

from setuptools import setup, find_packages


def __get_version():
    with open("quart_discord/__init__.py") as package_init_file:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', package_init_file.read(), re.MULTILINE).group(1)


requirements = [
    'Quart',
    'pyjwt',
    'oauthlib',
    'Async-OAuthlib',
    'cachetools',
]

with open("README.md") as fh:
    long_description = fh.read()

on_rtd = os.getenv('READTHEDOCS') == 'True'
if on_rtd:
    requirements.append('sphinxcontrib-napoleon')
    requirements.append('Pallets-Sphinx-Themes')

extra_requirements = {
    'docs': ['sphinx==1.8.3'],
    'discodpy': ['discord.py'],
    'pycord': ['py-cord'],
    'nextcord': ['nextcord == 2.0.0']
}


setup(
    name='Quart-Discord-any',
    version=__get_version(),
    url='https://github.com/Memotic/Quart-Discord-any',
    license='MIT',
    author='Philip Dowie',
    author_email='philip@jnawk.nz',
    maintainer="William Hatcher",
    maintainer_email="william@memotic.net",
    description='Discord OAuth2 extension for Quart using modern Discord Libraries.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=requirements,
    extras_require=extra_requirements,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Programming Language :: Python :: 3",
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires='>=3.8',
)
