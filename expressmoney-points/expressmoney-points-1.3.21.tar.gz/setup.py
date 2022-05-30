"""
py setup.py sdist
twine upload dist/expressmoney-points-1.3.21.tar.gz
"""
import setuptools

setuptools.setup(
    name='expressmoney-points',
    packages=setuptools.find_packages(),
    version='1.3.21',
    description='Service points',
    author='Development team',
    author_email='dev@expressmoney.com',
    install_requires=('expressmoney',),
    python_requires='>=3.7',
)
