# pyhamtools

Pyhamtools is a set of functions and classes for Amateur Radio purpose. Currently the core part is the Callsign
Lookup which decodes any amateur radio callsign string and provides the corresponding information (Country, DXCC entity,
CQ Zone...etc). This basic functionality is needed for Logbooks, DX-Clusters or Log Checking.

Currently,
* [Country-Files.org](http://country-files.org)
* [Clublog Prefixes & Exceptions XML File](https://clublog.freshdesk.com/support/articles/54902-downloading-the-prefixes-and-exceptions-as)
* [Clublog DXCC Query API](http://clublog.freshdesk.com/support/articles/54904-how-to-query-club-log-for-dxcc)
* [Redis.io](http://redis.io)

are supported sources.
All services can be accessed through a unified interface.

## References
This Library is used in production at the [DXHeat.com DX Cluster](https://dxheat.com), performing several thousand
lookups per day.

## Documentation
Check out the full documentation at:
[PyHamTools.readthedocs.org](http://pyhamtools.readthedocs.org/en/latest/index.html)

## Installation

Easiest way to install pyhamtools is through the packet manager PIP:
`pip install pyhamtools`

## Example: How to use pyhamtools

```
>>> from pyhamtools import LookupLib, Callinfo
>>> my_lookuplib = LookupLib(lookuptype="countryfile")
>>> cic = Callinfo(my_lookuplib)
>>> cic.get_all("DH1TW")
    {
        'country': 'Fed. Rep. of Germany',
        'adif': 230,
        'continent': 'EU',
        'latitude': 51.0,
        'longitude': -10.0,
        'cqz': 14,
        'ituz': 28
    }

```

## Testing
An extensive set of unit tests has been created for all Classes & Methods.