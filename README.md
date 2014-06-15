# pyhamtools

A Library with Amateur Radio specific Functions and Classes for any kind of Callsign Lookup Service, e.g. Logbooks
or DX-Clusters. Currently,
* [Country-Files.org](http://country-files.org),
* [Clublog Prefixes & Exceptions XML File](https://clublog.freshdesk.com/support/articles/54902-downloading-the-prefixes-and-exceptions-as)
* [Clublog DXCC Query API](http://clublog.freshdesk.com/support/articles/54904-how-to-query-club-log-for-dxcc)
* [Redis.io](http://redis.io)
are supported sources.
All services can be accessed through a unified interface.

This Library is used in production at DxHeat.com.

# Installation

Easiest way to install pyhamtools is through the packet manager PIP:
`pip install pyhamtools'

# How to use pyhamtools

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

Check out the full documentation at:
[PyHamTools.readthedocs.org](pyhamtools.readthedocs.org/en/latest/index.html)