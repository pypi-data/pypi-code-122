from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name='bgdistbluehigh',
      version='0.2',
      description='Binomial and Gaussian distributions',
      license="MIT",
      long_description=long_description,
      author='Sachin R',
      packages=find_packages('bgdistbluehigh'),
      zip_safe=False)