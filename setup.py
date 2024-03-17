#!/usr/bin/env python
import os
from setuptools import setup

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
          "requests>=2.21.0",
          "ephem>=4.1.3",
          "beautifulsoup4>=4.7.1",
          "lxml>=4.8.0,<5.0.0",
          "redis>=2.10.6",
      ],
      **kw
     )
