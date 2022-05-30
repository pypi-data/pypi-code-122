from setuptools import setup
import os

setup(
    name='changelog-generator-ciena',
    version='0.0.1a1',
    url='https://git.eng.blueplanet.com/ci-cd/changelog-generator',
    license='Ciena',
    author='Akshay',
    author_email='aksrivas@ciena.com',
    description='Changelog generator tool',
    long_description='',
    package_dir={'': 'src'},
    py_modules=["changeLogGenerator"]

)
