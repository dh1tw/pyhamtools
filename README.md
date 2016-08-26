# pyhamtools

[![Join the chat at https://gitter.im/dh1tw/pyhamtools](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/dh1tw/pyhamtools?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Pyhamtools is a set of functions and classes for Amateur Radio purpose. Currently the core part is the Callsign
Lookup which decodes any amateur radio callsign string and provides the corresponding information (Country, DXCC entity,
CQ Zone...etc). This basic functionality is needed for Logbooks, DX-Clusters or Log Checking.

Currently,
* [Country-Files.org](http://country-files.org)
* [Clublog Prefixes & Exceptions XML File](https://clublog.freshdesk.com/support/articles/54902-downloading-the-prefixes-and-exceptions-as)
* [Clublog DXCC Query API](http://clublog.freshdesk.com/support/articles/54904-how-to-query-club-log-for-dxcc)
* [QRZ.com XML API](http://www.qrz.com/XML/current_spec.html)
* [Redis.io](http://redis.io)

are supported sources.
All these lookup services can be accessed through a unified interface.

Other modules include location based calculations (e.g. distance, heading between Maidenhead locators) or
frequency based calculations (e.g. frequency to band).

## References
This Library is used in production at the [DXHeat.com DX Cluster](https://dxheat.com), performing several thousand
lookups and calculations per day.

## Documentation
Check out the full documentation at:
[PyHamTools.readthedocs.org](http://pyhamtools.readthedocs.org/en/latest/index.html)

## License
PyHamTools are published under the permissive [MIT License](http://choosealicense.com/licenses/mit/). You can find a good comparison of Open Source Software licenses, including the MIT license at [choosealicense.com](http://choosealicense.com/licenses/)

[PyHamTools.readthedocs.org](http://pyhamtools.readthedocs.org/en/latest/index.html)

## Installation

Easiest way to install pyhamtools is through the packet manager PIP:

`pip install pyhamtools`

## Example: How to use pyhamtools

```

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
        'longitude': -10.0,
        'cqz': 14,
        'ituz': 28
    }

```

## Testing
An extensive set of unit tests has been created for all Classes & Methods.
