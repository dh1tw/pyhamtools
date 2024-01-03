# pyhamtools

![Build Status](https://github.com/dh1tw/pyhamtools/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/dh1tw/pyhamtools/branch/master/graph/badge.svg)](https://codecov.io/gh/dh1tw/pyhamtools)
[![PyPI version](https://badge.fury.io/py/pyhamtools.svg)](https://badge.fury.io/py/pyhamtools)

Pyhamtools is a set of functions and classes for Amateur Radio purposes.
Currently, the core part is the Callsign Lookup which decodes any amateur radio
callsign string and provides the corresponding information (Country, DXCC
entity, CQ Zone...etc). This basic functionality is needed for Logbooks,
DX-Clusters or Log Checking. This and additional convenience features are
provided for the following sources:

Currently,
* [AD1C's Amateur Radio Country Files](https://www.country-files.com)
* [Clublog Prefixes & Exceptions XML File](https://clublog.freshdesk.com/support/articles/54902-downloading-the-prefixes-and-exceptions-as)
* [Clublog DXCC Query API](http://clublog.freshdesk.com/support/articles/54904-how-to-query-club-log-for-dxcc)
* [QRZ.com XML API](http://www.qrz.com/XML/current_spec.html)
* [Redis.io](http://redis.io)
* [ARRL Logbook of the World (LOTW)](https://lotw.arrl.org)
* [eQSL.cc user list](https://www.eqsl.cc)
* [Clublog & OQRS user list](http://clublog.freshdesk.com/support/solutions/articles/3000064883-list-of-club-log-and-lotw-users)

Other modules include location-based calculations (e.g. distance,
heading between Maidenhead locators) or frequency-based calculations
(e.g. frequency to band).

## References

This Library is used in production at the [DXHeat.com DX Cluster](https://dxheat.com), performing several thousand lookups and calculations per day.

## Compatibility

Pyhamtools is compatible with Python >=3.6.
We check compatibility on OSX, Windows, and Linux with the following Python versions:

* Python 3.6 (will be deprecated in 2024)
* Python 3.7 (will be deprecated in 2024)
* Python 3.8
* Python 3.9
* Python 3.10
* Python 3.11
* Python 3.12
* [pypy3.7](https://pypy.org/) (will be deprecated in 2024)
* [pypy3.8](https://pypy.org/)
* [pypy3.9](https://pypy.org/)
* [pypy3.10](https://pypy.org/)

The support for Python 2.7 and 3.5 has been deprecated at the end of 2023. The last version which supports Python 2.7 and Python 3.5 is 0.8.7.

## Documentation

Check out the full documentation including the changelog at:
[pyhamtools.readthedocs.org](http://pyhamtools.readthedocs.org/en/latest/index.html)

## License

Pyhamtools is published under the permissive [MIT License](http://choosealicense.com/licenses/mit/). You can find a good comparison of
Open Source Software licenses, including the MIT license at [choosealicense.com](http://choosealicense.com/licenses/)

## Dependencies

Starting with version 0.8.0, `libxml2-dev` and `libxslt-dev` are required dependencies.

There is a good change that the libraries are already installed on your system. If not, you can install them with the package manager of your distro. For example on Debian / Ubuntu based distros the corresponding command is:

```bash

$ sudo apt-get install libxml2-dev libxslt-dev

```

You don't need to install these libraries manually on Windows / MacOS.


## Installation


The easiest way to install pyhamtools is through the packet manager `pip`:

```bash

$ pip install pyhamtools

```

Christoph, [@df7cb](https://github.com/df7cb) is kindly maintaining a Debian package as an alternative way to install pyhamtools:

```bash

$ sudo apt-get install pyhamtools

```

## Example: How to use pyhamtools

``` python

>>> from pyhamtools.locator import calculate_heading
>>> calculate_heading("JN48QM", "QF67bf")
74.3136


>>> from pyhamtools import LookupLib, Callinfo
>>> my_lookuplib = LookupLib(lookuptype="countryfile")
>>> cic = Callinfo(my_lookuplib)
>>> cic.get_all("DH1TW")
    {
        'country': 'Fed. Rep. of Germany',
        'adif': 230,
        'continent': 'EU',
        'latitude': 51.0,
        'longitude': 10.0,
        'cqz': 14,
        'ituz': 28
    }

```

## Testing

An extensive set of unit tests has been created for all Classes & Methods.
To be able to perform all tests, you need a QRZ.com account and a
[Clublog API key](http://clublog.freshdesk.com/support/solutions/articles/54910-api-keys).

pyhamtools rely on the [pytest](https://docs.pytest.org/en/latest/) testing
framework. To install it with all the needed dependencies run:

```bash

$ pip install -r requirements-pytest.txt

```

The QRZ.com credentials and the Clublog API key have to be set in the environment
variables:

```bash

$ export CLUBLOG_APIKEY="<your API key>"
$ export QRZ_USERNAME="<your qrz.com username>"
$ export QRZ_PWD="<your qrz.com password>"

```

To perform the tests related to the [redis](https://redis.io/) key/value
store, a Redis server has to be up & running.

```bash

$ sudo apt install redis-server
$ redis-server

```

To run the tests, simply execute:

```bash

$ pytest --cov pyhamtools

```

## Generate the documentation

You can generate the documentation of pyhamtools with the following commands:

```bash

$ pip install -r requirements-docs.txt
$ cd docs
$ make html

```