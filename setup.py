#!/usr/bin/env python
import sys
import os
from distutils.core import setup
# from pyhamtools import __version__, __release__

kw = {}

if sys.version_info >= (3,):
    kw['use_2to3'] = True

exec(open(os.path.join("pyhamtools","version.py")).read())

# from pyhamtools import __version__, __release__

setup(name='pyhamtools',
      version=__release__,
      description='Collection of Tools for Amateur Radio developers',
      author='Tobias Wellnitz, DH1TW',
      author_email='Tobias@dh1tw.de',
      url='http://github.com/dh1tw/pyhamtools',
      package_data={'': ['countryfilemapping.json']},
      packages=['pyhamtools'],
      install_requires=[
          "pytz", 
          "requests",
          "pyephem",
          "beautifulsoup4",
      ],
      **kw
     )
