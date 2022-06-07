from setuptools import setup, find_packages

with open("README", 'r') as f:
    long_description = f.read()

setup(name='bgdistskyhigh',
      version='0.1',
      description='Binomial and Gaussian distributions',
      license="MIT",
      long_description=long_description,
      author='Sachin R',
      packages=find_packages('bgdistskyhigh'),
      install_requires=['matplotlib'],
      zip_safe=False)