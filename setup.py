try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'name': 'Titsly'
  'description': 'Titsly is a url shortening python server',
  'author': 'Shadrach Tayo',
  'url': 'titsly.com',
  'author_email': 'shadrachtemitayo@gmail.com',
  'version': '0.1',
  'install_requires': ['nose'],
  'packages': [],
  'scripts': []
}

setup(**config)