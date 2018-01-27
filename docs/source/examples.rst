
Examples
========

Almost each class / function in the reference section has an example. For the sake of convenience, some examples are shown below to give you a quick understanding how PyHamTools work.

Calculate Shortpath and Longpath Heading between two locators
-------------------------------------------------------------

.. code-block:: none

   >>> from pyhamtools.locator import calculate_heading, calculate_heading_longpath
   >>> calculate_heading("JN48QM", "QF67bf")
   74.3136
   
   >>> calculate_heading_longpath("JN48QM", "QF67bf")
   254.3136


Calculate Distance between two WGS84 Coordinates
------------------------------------------------

.. code-block:: none

   >>> from pyhamtools.locator import calculate_distance, latlong_to_locator
   >>> locator1 = latlong_to_locator(48.52, 9.375)
   >>> locator2 = latlong_to_locator(-32.77, 152.125)
   >>> distance = calculate_heading(locator1, locator2)
   >>> print("%.1fkm" % distance)
   16466.4km
   
Calculate Sunrise and Sunset for JN48QM on the 1. January 2015
--------------------------------------------------------------


.. code-block:: none

   >>> from pyhamtools.locator import calculate_sunrise_sunset
   >>> from datetime import datetime
   >>> my_locator = "JN48QM"
   >>> my_date = datetime(year=2015, month=1, day=1)
   >>> data = calculate_sunrise_sunset(my_locator, my_date)
   >>> print "Sunrise: " + data['sunrise'].strftime("%H:%MZ") + ", Sunset: " + data['sunset'].strftime("%H:%MZ")
   Sunrise: 07:14Z, Sunset: 16:15Z


Decode a Callsign and get Country name, ADIF ID, Latitude & Longitude
---------------------------------------------------------------------

In this example we will use AD1C's Country-files.com database to perform the lookup.

First we need to instanciate a LookupLib object for Country-files.com database. The latest database will be downloaded automatically.

.. code-block:: none

   >>> from pyhamtools import LookupLib, Callinfo
   >>> my_lookuplib = LookupLib(lookuptype="countryfile")
   
   
Next, a Callinfo object needs to be instanciated. The lookuplib object will be injected on construction.

.. code-block:: none

   >>> cic = Callinfo(my_lookuplib)


Now we can query the information conveniently through our Callinfo object:

.. code-block:: none

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
