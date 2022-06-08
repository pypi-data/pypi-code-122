from setuptools import setup, find_packages

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License'
]

setup(name='quote_Extract',
      version='0.0.1',
      description='Get a variety of Motivational Quotes here',
      url='',
      long_description = long_description,
      author='Ndongmo Christian',
      author_email='christainhonore2003@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      classifiers = classifiers,
      
      )