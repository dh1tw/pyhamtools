# pyhamtools

Linux & MacOS [![Build Status](https://travis-ci.org/dh1tw/pyhamtools.svg?branch=master)](https://travis-ci.org/dh1tw/pyhamtools)
Windows [![Build status](https://ci.appveyor.com/api/projects/status/it6077sklplhgkyf?svg=true)](https://ci.appveyor.com/project/dh1tw/pyhamtools)


Pyhamtools is a set of functions and classes for Amateur Radio purpose.
Currently the core part is the Callsign Lookup which decodes any amateur radio
callsign string and provides the corresponding information (Country, DXCC
entity, CQ Zone...etc). This basic functionality is needed for Logbooks,
DX-Clusters or Log Checking. This and additional convenience features are
provided for the following sources:

Currently,
* [AD1C's Country-Files.org](http://country-files.org)
* [Clublog Prefixes & Exceptions XML File](https://clublog.freshdesk.com/support/articles/54902-downloading-the-prefixes-and-exceptions-as)
* [Clublog DXCC Query API](http://clublog.freshdesk.com/support/articles/54904-how-to-query-club-log-for-dxcc)
* [QRZ.com XML API](http://www.qrz.com/XML/current_spec.html)
* [Redis.io](http://redis.io)
* [ARRL Logbook of the World (LOTW)](http://https://lotw.arrl.org)
* [eQSL.cc user list](https://www.eqsl.cc)
* [Clublog & OQRS user list](http://clublog.freshdesk.com/support/solutions/articles/3000064883-list-of-club-log-and-lotw-users)

Other modules include location based calculations (e.g. distance,
heading between Maidenhead locators) or frequency based calculations
(e.g. frequency to band).

## References

This Library is used in production at the [DXHeat.com DX Cluster](https://dxheat.com), performing several thousand lookups and calculations per day.

## Compatibility

Pyhamtools is since version 0.6.0 compatible with > Python 2.7 and > python 3.3.
We check compatibility on OSX, Windows and Linux with the following Python
versions:

* Python 2.7
* Python 3.3
* Python 3.4
* Python 3.5
* Python 3.6
* [pypy](https://pypy.org/) (Python 2)

## Documentation

Check out the full documentation including the changelog at:
[pyhamtools.readthedocs.org](http://pyhamtools.readthedocs.org/en/latest/index.html)

## License

Pyhamtools is published under the permissive [MIT License](http://choosealicense.com/licenses/mit/). You can find a good comparison of
Open Source Software licenses, including the MIT license at [choosealicense.com](http://choosealicense.com/licenses/)

## Installation

Easiest way to install pyhamtools is through the packet manager `pip`:

```bash

$ pip install pyhamtools

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
In order to be able to perform all tests you need a QRZ.com account and a
[Clublog API key](http://clublog.freshdesk.com/support/solutions/articles/54910-api-keys).

pyhamtools rely on the [pytest](https://docs.pytest.org/en/latest/) testing
framework. In order to install it with all the needed dependencies run:

```bash

$ pip install -r requirements-pytest.txt

```

The QRZ.com credentials and the Clublog API key have to be set in environment
variables:

```bash

$ export CLUBLOG_APIKEY="<your API key>"
$ export QRZ_USERNAME="<your qrz.com username>"
$ export QRZ_PWD="<your qrz.com password>"

```

To run the tests, simply execute:

```bash

$ pytest

```

## Generate the documentation

You can generate the documentation of pyhamtools with the following commands:

```bash

$ pip install -r requirements-docs.txt
$ cd docs
$ make html

```