Changelog
---------

PyHamtools 0.11.0
================

02. March 2025

* added support for Python 3.13 

PyHamtools 0.10.0
================

01. June 2024

* full support for 4, 6, 8 characters Maidenhead locator conversions


PyHamtools 0.9.1
================

17. March 2024

* switched from distutils to setuptools. No impact for endusers.


PyHamtools 0.9.0
================

28. December 2023

* Deprecated support for Python 2.7 and Python 3.5
* Added Support for Python 3.12
* Replaced pytz with datetime.timezone
* Added Continous Integration Jobs for MacOS (now supported by Github Actions)


PyHamtools 0.8.7
================

31. December 2022

* Lookuplib/Countryfiles: corrected Brazil to ADIF country id 108
* Lookuplib/Countryfiles: corrected Domenican Republic to ADIF country if 72
* Changed the remaining Clublog URLs to https://cdn.clublog.org 

PyHamtools 0.8.6
================

26. December 2022

* fixed regex regression for detection two-by-one callsigns

PyHamtools 0.8.5
================

26. December 2022

* refined regex for decoding callsigns. In particular to better recognize callsigns with one or more digits in the suffix (e.g. TI5N5BEK, DP44N44T)


PyHamtools 0.8.4
================

18. December 2022

* raise KeyError when callsigns contain non-latin characters (e.g. cyrillic letters)


PyHamtools 0.8.3
================

06. December 2022

* fixed XML parsing error in QRZ.com session key renewal


PyHamtools 0.8.2
================

05. December 2022

* timezone field from QRZ.com casted to str instead of int


PyHamtools 0.8.1
================

05. December 2022

* removed debug print statement from QRZ.com queries


PyHamtools 0.8.0
================

05. December 2022

* Finally switched to XML parser in BeautifulSoup for qrz.com (requires libxml2-dev and libxslt-dev packages!)
* Fixed minor bug in parsing the CCC field of qrz.com XML messages
* Fixed VK9XX test fixture (Latitude & Longitude)
* Added support for CPython 3.10 and 3.11
* Added support for PyPy 3.7, 3.8, 3.9
* Dropped support for Python 3.4
* Fixed regular expression escapings which were marked as deprecated (since Python 3.6)
* Replaced legacy execfile function in test package to remove the deprecation warning about 'imp'


PyHamtools 0.7.10
================

12. May 2022

* Using lxml to parse XML messages returned from qrz.com
* Upgraded dependencies


PyHamtools 0.7.9
================

16. December 2021

* Calculating sunrise and sunset close to the artic region raised a ValueError due
  to a bug in the underlying 3rd party library ephem. This release upgrades the 
  dependency to ephem > 4.1.3 which has the bug already fixed.

PyHamTools 0.7.8
================

04. December 2021

* Updated Clublog's (CDN based) URL for downloading the Prefixes and Exceptions XML 

PyHamTools 0.7.7
================

01. June 2021

* Added support for Python 3.9
* Added deprecation warnings for Python 3.4 and 3.5


PyHamTools 0.7.6
================

29. September 2020

 * Renamed "Kingdom of eSwatini" into "Kingdom of Eswatini" (#19 tnx @therrio)
 * fixed the latitude in the VK9XX unit test fixture
 * fixed docs - redis related example in docstring (#20 tnx @kholia)
 * fixed docs - calculate distance example (#18 tnx @devnulling)


PyHamTools 0.7.5
================

3. March 2020

 * fixed a bug related to badly escaped JSON data when using redis
 * lookup data is now copied approx. 5x faster into redis
 * download artifacts are now cleaned up from the temporary download directory

PyHamTools 0.7.4
================

27. November 2019

 * Renamed "Swaziland" into "Kingdom of eSwatini"


PyHamTools 0.7.3
================

30. May 2019

 * fixed dependency redis dependency to use at least a version compatible with python 2.7.


PyHamTools 0.7.2
================

29. May 2019

 * Changed Macedonia to North Macedonia
 * Updated test fixtures
 * bumped dependencies to current versions

PyHamTools 0.7.1
================

21. May 2018

 * Refined FT8 frequencies


PyHamTools 0.7.0
================

20. May 2018
 * Added FT8 frequencies as DIGITAL
 * Updated test fixtures
 * Minor fixes wrt Kosovo & AD1C Countryfiles


PyHamTools 0.6.1
================

28. January 2018
 * Minor bugfix for lookuplib which used with country-files.com


PyHamTools 0.6.0
================

23. January 2018

 * Support for Python3 has been added
 * CI pipeline setup. Compatibility of Pyhamtools is now checked on Windows and
   Linux for Python 2.7, 3.4, 3.5, 3.6 and pypy
 * BREAKING CHANGE: Longitude is now provided with the correct sign for all
   lookup libraries. The AD1C cty format used by Countryfile and ClublogAPI
   provide the longitude with the wrong sign. This is now covered and internally
   corrected. East = positive longitude, West = negative longitude.
 * Added a function to download the Clublog user list and the associated activity dates
 * updated requirements for libraries used by pyhamtools
 * some slow regex were replaced by faster string based lookups


PyHamTools 0.5.6
================

20. August 2017

 * LOTW User list is now downloaded directly from ARRL



PyHamTools 0.5.5
================

18. August 2016

 * Refined callsign detection rule for two digit prefix with appendix (e.g. 7N0ERX/1)
 * Refined callsign detection rule for callsigns with two appendixes (e.g. SV8GXQ/P/QRP)



PyHamTools 0.5.4
================

11. January 2016

 * Bugfix: Callinfo.get_all(callsign, timestamp) did ignore timestamp
 * added unit test for the bug above
 * extended timeout for QRZ.com request to 10 seconds (sometimes a bit slow)
 * updated QRZ.com unit tests for fixture callsigns (XX1XX and XX2XX)


PyHamTools 0.5.3
================

30. December 2015

 * Updated DXCC entity name of ZL9 (arrl id 16) from Auckland & Campbell to "N.Z. Subantarctic Is." in countrymapping.json (tnx G0UKB)
 * Deleted "Auckland" (016) from countrymapping.json
 * corrected code example of latlong_to_locator() (tnx VE5ZX)

PyHamTools 0.5.2
================

14. April 2015

 * catching another bug related to QRZ.com sessions



PyHamTools 0.5.1
================

13. April 2015

 * improved handling of expired QRZ.com sessions


PyHamTools 0.5.0
================

5. April 2015

 * implemented QRZ.com interface into LookupLib [LookupLib]

 * changed and unified all output to Unicode

 * corrected Longitude to General Standard (-180...0° West, 0...180° East) [LookupLib]

 * improved callsign decoding algorithm [CallInfo]

 * added special case to decode location of VK9 callsigns [CallInfo]

 * added handling of special callsigns which can't be decoded properly inside a separate callsign exception file (e.g. 7QAA) [CallInfo]

 * added ValueError when LOTW data from file contains too many errors [qsl]


PyHamTools 0.4.2
================

11. October 2014

 * added pyhamtools.qsl (get EQSL.cc and LOTW user lists)

PyHamTools 0.4.1
================

27. September 2014

 * short calls in different countries (e.g. 9H3A/C6A) are now decoded correctly

 * added pyhamtools.frequency

 * moved pyhamtools.utils.freq_to_band into pyhamtools.frequency

 * deprecated module pyhamtools.utils

PyHamTools 0.4.0
================

20. September 2014

 * Added module for locator based calculations (pyhamtools.locators)
