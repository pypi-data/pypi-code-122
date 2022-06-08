from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='FLHT',
  version='0.0.1',
  description='Fourier, Laplace, Hankel Transform calculator of Functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Adarsh Gangwar',
  author_email='adarsh.phy22@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Transforms calculator', 
  packages=find_packages(),
  install_requires=['scipy', 'numpy', 'matplotlib', 'math'] 
)