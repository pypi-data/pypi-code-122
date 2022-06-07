
from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Math-Parser',
    version='0.1.2',
    description='This package evaluates mathematics expressions written in string safely.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Victor Soeiro',
    author_email='victor.soeiro.araujo@gmail.com',
    url='https://github.com/victor-soeiro/Math-Parser',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
    ],
    packages=find_packages(),
    install_requires=[],
    python_requires='>=3.6',
    keywords=[
        'mathematics', 'expressions', 'compilers', 'evaluation'
    ]
)
