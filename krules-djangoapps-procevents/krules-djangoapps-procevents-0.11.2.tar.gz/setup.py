from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='krules-djangoapps-procevents',
version="0.11.2",    author="Airspot",
    author_email="info@arispot.tech",
    license="Apache Licence 2.0",
    keywords="krules knative",
    url="https://github.com/airspot-dev/krules",
    packages=find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>3.8',
    install_requires=[
        'krules-djangoapps-common==0.11.2',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)