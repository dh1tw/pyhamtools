Changelog
---------

PyHamTools 0.5.1
================

14. April 2015

 * improved handling of expired QRZ.com sessions


PyHamTools 0.5.0
================

5. April 2015

 * implemented QRZ.com interface into LookupLib [LookupLib]

 * changed and unified all output to Unicode
 
 * corrected Longitude to General Standard (-180...0° West, 0...180° East) [LookupLib]
 
 * improved callsign decoding alogrithm [CallInfo]
 
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
