#!/usr/bin/env python
import sys
import os
from distutils.core import setup

kw = {}

exec(open(os.path.join("pyhamtools","version.py")).read())

setup(name='pyhamtools',
      version=__release__,
      description='Collection of Tools for Amateur Radio developers',
      author='Tobias Wellnitz, DH1TW',
      author_email='Tobias@dh1tw.de',
      url='http://github.com/dh1tw/pyhamtools',
      package_data={'': ['countryfilemapping.json']},
      packages=['pyhamtools'],
      install_requires=[
          "pytz>=2017.3",
          "requests>=2.18.4",
          "pyephem>=3.7.6.0",
          "beautifulsoup4>=4.6.0",
          "future>=0.16.0",
          "redis>=2.10.6",
      ],
      **kw
     )
