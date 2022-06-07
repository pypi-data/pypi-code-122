from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.md')).read()
except IOError:
    README = ''

version = "0.1.0"

setup(
    name='game_coroutines',
    version=version,
    description="game_coroutines is a pure-python lib with no dependencies, to simplify calling methods over time on game environments.",
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=['Development Status :: 5 - Production/Stable',],  # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='pygame arcade coroutines routines sprites',
    author='Leonardo Baptista',
    author_email='leonardoobaptistaa@gmail.com',
    url='https://github.com/Ruppy/game_coroutines',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    py_modules='game_coroutines',
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    ],
    entry_points={},
)
