import os
from setuptools import setup

# from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(
    os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir))
)

setup(
    name='systemd_service',
    version='1.8',
    packages=['systemd_service'],
    author='Yeison Cardona',
    author_email='yeisoneng@gmail.com',
    maintainer='Yeison Cardona',
    maintainer_email='yeisoneng@gmail.com',
    # url='http://yeisoncardona.com/',
    download_url='https://github.com/UN-GCPDS/systemd-service',
    install_requires=[],
    include_package_data=True,
    license='BSD-2-Clause',
    description="Simple API to automate the creation of custom daemons for GNU/Linux.",
    long_description=README,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
