#!/usr/bin/env python
import sys
from distutils.core import setup

kw = {}

if sys.version_info >= (3,):
    kw['use_2to3'] = True

setup(name='pyhamtools',
      version='0.1.1',
      description='Collection of Tools for Amateur Radio developers',
      author='Tobias Wellnitz, DH1TW',
      author_email='Tobias@dh1tw.de',
      url='http://github.com/dh1tw/pyhamtools',
      packages=['pyhamtools'],
      install_requires=[
          "pytz", 
          "requests",
      ],
      **kw
     )
