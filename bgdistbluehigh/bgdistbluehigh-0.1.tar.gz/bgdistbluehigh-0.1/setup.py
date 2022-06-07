from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='bgdistbluehigh',
      version='0.1',
      description='Binomial and Gaussian distributions',
      license="MIT",
      long_description=long_description,
      author='Sachin R',
      packages=find_packages('bgdistbluehigh'),
      install_requires=['matplotlib'],
      zip_safe=False)