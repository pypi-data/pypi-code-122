from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import os

from setuptools import setup, find_packages

install_requires = ['numpy>=1.17.2', 'torch>=1.7.0', 'scipy==1.6.0', 'pandas>=1.0.5', 'tqdm>=4.48.2',
                    'colorlog==4.7.2','colorama==0.4.4',
                    'scikit_learn>=0.23.2', 'pyyaml>=5.1.0', 'tensorboard>=2.5.0', 'recbole>=1.0.0']

setup_requires = []

extras_require = {
    'hyperopt': ['hyperopt>=0.2.4']
}

classifiers = ["License :: OSI Approved :: MIT License"]

long_description = 'RecBole-CDR is developed based on RecBole for ' \
                   'reproducing and developing cross-domain-recommendation ' \
                   'algorithms in a unified, comprehensive and efficient framework ' \
                   'for research purpose. In the first version, our library ' \
                   'includes 10 cross-domain-recommendation algorithms. '\

# Readthedocs requires Sphinx extensions to be specified as part of
# install_requires in order to build properly.
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    install_requires.extend(setup_requires)

setup(
    name='recbole-cdr',
    version=
    '0.1.0', 
    description='A unified, comprehensive and efficient cross-domain-recommendation library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/RUCAIBox/RecBole-CDR',
    author='RecBoleTeam',
    author_email='recbole@outlook.com',
    packages=[
        package for package in find_packages()
        if package.startswith('recbole_cdr')
    ],
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    extras_require=extras_require,
    zip_safe=False,
    classifiers=classifiers,
)