import re
import logging
from datetime import datetime
import sys

import pytz

from pyhamtools.consts import LookupConventions as const

from pyhamtools.callsign_exceptions import callsign_exceptions

UTC = pytz.UTC
timestamp_now = datetime.utcnow().replace(tzinfo=UTC)

if sys.version_info < (2, 7, ):
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass


class Callinfo(object):
    """
    The purpose of this class is to return data (country, latitude, longitude, CQ Zone...etc) for an
    Amateur Radio callsign. The class can be used with any lookup database,
    provided through an Instance of :py:class:`LookupLib`.
    An instance of :py:class:`Lookuplib` has to be injected on object construction.

    Args:
        lookuplib (:py:class:`LookupLib`) : instance of :py:class:`LookupLib`
        logger (logging.getLogger(__name__), optional): Python logger

    """

    def __init__(self, lookuplib, logger=None):

        self._logger = None
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger(__name__)
            if sys.version_info[:2] == (2, 6):
                self._logger.addHandler(NullHandler())
            else:
                self._logger.addHandler(logging.NullHandler())

        self._lookuplib = lookuplib
        self._callsign_info = None

    @staticmethod
    def get_homecall(callsign):
        """Strips off country prefixes (HC2/DH1TW) and activity suffixes (DH1TW/P).

        Args:
            callsign (str): Amateur Radio callsign

        Returns:
            str: callsign without country/activity pre/suffixes

        Raises:
            ValueError: No callsign found in string

        Example:
            The following code retrieves the home call for "HC2/DH1TW/P"

            >>> from pyhamtools import LookupLib, Callinfo
            >>> my_lookuplib = LookupLib(lookuptype="countryfile")
            >>> cic = Callinfo(my_lookuplib)
            >>> cic.get_homecall("HC2/DH1TW/P")
            DH1TW

        """

        callsign = callsign.upper()
        homecall = re.search('[\d]{0,1}[A-Z]{1,2}\d([A-Z]{1,4}|\d{3,3}|\d{1,3}[A-Z])[A-Z]{0,5}', callsign)
        if homecall:
            homecall = homecall.group(0)
            return homecall
        else:
            raise ValueError

    def _iterate_prefix(self, callsign, timestamp=timestamp_now):
        """truncate call until it corresponds to a Prefix in the database"""
        prefix = callsign

        if re.search('(VK|AX|VI)9[A-Z]{3}', callsign): #special rule for VK9 calls
            if timestamp > datetime(2006,1,1, tzinfo=UTC):
                prefix = callsign[0:3]+callsign[4:5]

        while len(prefix) > 0:
            try:
                return self._lookuplib.lookup_prefix(prefix, timestamp)
            except KeyError:
                prefix = prefix.replace(' ', '')[:-1]
                continue
        raise KeyError

    @staticmethod
    def check_if_mm(callsign):
        check = callsign[-3:].upper()
        return "/MM" in check

    @staticmethod
    def check_if_am(callsign):
        check = callsign[-3:].upper()
        return "/AM" in check

    @staticmethod
    def check_if_beacon(callsign):
        check = callsign[-4:].upper()
        return "/B" in check or "/BCN" in check

    def _dismantle_callsign(self, callsign, timestamp=timestamp_now):
        """ try to identify the callsign's identity by analyzing it in the following order:

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Raises:
            KeyError: Callsign could not be identified


        """
        entire_callsign = callsign.upper()

        if re.search('[/A-Z0-9\-]{3,15}', entire_callsign):  # make sure the call has at least 3 characters

            if re.search('\-\d{1,3}$', entire_callsign):  # cut off any -10 / -02 appendixes
                callsign = re.sub('\-\d{1,3}$', '', entire_callsign)

            if re.search('/[A-Z0-9]{1,4}/[A-Z0-9]{1,4}$', callsign):
                callsign = re.sub('/[A-Z0-9]{1,4}$', '', callsign)  # cut off 2. appendix DH1TW/HC2/P -> DH1TW/HC2

            # multiple character appendix (callsign/xxx)
            if re.search('[A-Z0-9]{4,10}/[A-Z0-9]{2,4}$', callsign):  # case call/xxx, but ignoring /p and /m or /5
                appendix = re.search('/[A-Z0-9]{2,4}$', callsign)
                appendix = re.sub('/', '', appendix.group(0))
                self._logger.debug("appendix: " + appendix)

                if appendix == 'MM':  # special case Martime Mobile
                    #self._mm = True
                    return {
                        'adif': 999,
                        'continent': '',
                        'country': 'MARITIME MOBILE',
                        'cqz': 0,
                        'latitude': 0.0,
                        'longitude': 0.0
                    }
                elif appendix == 'AM':  # special case Aeronautic Mobile
                    return {
                        'adif': 998,
                        'continent': '',
                        'country': 'AIRCAFT MOBILE',
                        'cqz': 0,
                        'latitude': 0.0,
                        'longitude': 0.0
                    }
                elif appendix == 'QRP':  # special case QRP
                    callsign = re.sub('/QRP', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)
                elif appendix == 'QRPP':  # special case QRPP
                    callsign = re.sub('/QRPP', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)
                elif appendix == 'BCN':  # filter all beacons
                    callsign = re.sub('/BCN', '', callsign)
                    data = self._iterate_prefix(callsign, timestamp).copy()
                    data[const.BEACON] = True
                    return data
                elif appendix == "LH":  # Filter all Lighthouses
                    callsign = re.sub('/LH', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)
                elif re.search('[A-Z]{3}', appendix): #case of US county(?) contest N3HBX/UAL
                    callsign = re.sub('/[A-Z]{3}$', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)

                else:
                    # check if the appendix is a valid country prefix
                    return self._iterate_prefix(re.sub('/', '', appendix), timestamp)

            # Single character appendix (callsign/x)
            elif re.search('/[A-Z0-9]$', callsign):  # case call/p or /b /m or /5 etc.
                appendix = re.search('/[A-Z0-9]$', callsign)
                appendix = re.sub('/', '', appendix.group(0))

                if appendix == 'B':  # special case Beacon
                    callsign = re.sub('/B', '', callsign)
                    data = self._iterate_prefix(callsign, timestamp).copy()
                    data[const.BEACON] = True
                    return data

                elif re.search('\d$', appendix):
                    area_nr = re.search('\d$', appendix).group(0)
                    callsign = re.sub('/\d$', '', callsign) #remove /number
                    if len(re.findall(r'\d+', callsign)) == 1: #call has just on digit e.g. DH1TW
                        callsign = re.sub('[\d]+', area_nr, callsign)
                    else: # call has several digits e.g. 7N4AAL
                        pass # no (two) digit prefix contries known where appendix would change entitiy
                    return self._iterate_prefix(callsign, timestamp)

                else:
                    return self._iterate_prefix(callsign, timestamp)

            # regular callsigns, without prefix or appendix
            elif re.match('^[\d]{0,1}[A-Z]{1,2}\d([A-Z]{1,4}|\d{3,3}|\d{1,3}[A-Z])[A-Z]{0,5}$', callsign):
                return self._iterate_prefix(callsign, timestamp)

            # callsigns with prefixes (xxx/callsign)
            elif re.search('^[A-Z0-9]{1,4}/', entire_callsign):
                pfx = re.search('^[A-Z0-9]{1,4}/', entire_callsign)
                pfx = re.sub('/', '', pfx.group(0))
                #make sure that the remaining part is actually a callsign (avoid: OZ/JO81)
                rest = re.search('/[A-Z0-9]+', entire_callsign)
                rest = re.sub('/', '', rest.group(0))
                if re.match('^[\d]{0,1}[A-Z]{1,2}\d([A-Z]{1,4}|\d{3,3}|\d{1,3}[A-Z])[A-Z]{0,5}$', rest):
                    return self._iterate_prefix(pfx)

        if entire_callsign in callsign_exceptions:
            return self._iterate_prefix(callsign_exceptions[entire_callsign])

        self._logger.debug("Could not decode " + callsign)
        raise KeyError("Callsign could not be decoded")

    def _lookup_callsign(self, callsign, timestamp=timestamp_now):

        # Check if operation is invalid
        invalid = False
        try:
            invalid = self._lookuplib.is_invalid_operation(callsign, timestamp)
            if invalid:
                raise KeyError
        except KeyError:
            if invalid:
                raise

        if self.check_if_mm(callsign):
            return {
                'adif': 999,
                'continent': '',
                'country': 'MARITIME MOBILE',
                'cqz': 0,
                'latitude': 0.0,
                'longitude': 0.0
            }
        elif self.check_if_am(callsign):
            return {
                'adif': 998,
                'continent': '',
                'country': 'AIRCAFT MOBILE',
                'cqz': 0,
                'latitude': 0.0,
                'longitude': 0.0
            }

        # Check if a dedicated entry/exception exists for the callsign
        try:
            data = self._lookuplib.lookup_callsign(callsign, timestamp).copy()
            if self.check_if_beacon(callsign):
                data[const.BEACON] = True
            return data
        except KeyError:
            pass

        # Dismantel the callsign and check if the prefix is known
        return self._dismantle_callsign(callsign, timestamp)

    def get_all(self, callsign, timestamp=timestamp_now):
        """ Lookup a callsign and return all data available from the underlying database

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            dict: Dictionary containing the callsign specific data

        Raises:
            KeyError: Callsign could not be identified

        Example:
            The following code returns all available information from the country-files.com database for the
            callsign "DH1TW"

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

        Note:
            The content of the returned data depends entirely on the injected
            :py:class:`LookupLib` (and the used database). While the country-files.com provides
            for example the ITU Zone, Clublog doesn't. Consequently, the item "ituz"
            would be missing with Clublog (API or XML) :py:class:`LookupLib`.

        """
        callsign_data = self._lookup_callsign(callsign, timestamp)

        try:
            cqz = self._lookuplib.lookup_zone_exception(callsign, timestamp)
            callsign_data[const.CQZ] = cqz
        except KeyError:
            pass

        return callsign_data

    def is_valid_callsign(self, callsign, timestamp=timestamp_now):
        """ Checks if a callsign is valid

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            bool: True / False

        Example:
            The following checks if "DH1TW" is a valid callsign

            >>> from pyhamtools import LookupLib, Callinfo
            >>> my_lookuplib = LookupLib(lookuptype="countryfile")
            >>> cic = Callinfo(my_lookuplib)
            >>> cic.is_valid_callsign("DH1TW")
            True

        """
        try:
            if self.get_all(callsign, timestamp):
                return True
        except KeyError:
            return False

    def get_lat_long(self, callsign, timestamp=timestamp_now):
        """ Returns Latitude and Longitude for a callsign

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            dict: Containing Latitude and Longitude

        Raises:
            KeyError: No data found for callsign

        Example:
            The following code returns Latitude & Longitude for "DH1TW"

            >>> from pyhamtools import LookupLib, Callinfo
            >>> my_lookuplib = LookupLib(lookuptype="countryfile")
            >>> cic = Callinfo(my_lookuplib)
            >>> cic.get_lat_long("DH1TW")
            {
                'latitude': 51.0,
                'longitude': -10.0
            }

        Note:
            Unfortunately, in most cases the returned Latitude and Longitude are not very precise.
            Clublog and Country-files.com use the country's capital coordinates in most cases, if no
            dedicated entry in the database exists. Best results will be retrieved with QRZ.com Lookup.

        """
        callsign_data = self.get_all(callsign, timestamp=timestamp)
        return {
            const.LATITUDE: callsign_data[const.LATITUDE],
            const.LONGITUDE: callsign_data[const.LONGITUDE]
        }

    def get_cqz(self, callsign, timestamp=timestamp_now):
        """ Returns CQ Zone of a callsign

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            int: containing the callsign's CQ Zone

        Raises:
            KeyError: no CQ Zone found for callsign

        """
        return self.get_all(callsign, timestamp)[const.CQZ]

    def get_ituz(self, callsign, timestamp=timestamp_now):
        """ Returns ITU Zone of a callsign

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            int: containing the callsign's CQ Zone

        Raises:
            KeyError: No ITU Zone found for callsign

        Note:
            Currently, only Country-files.com lookup database contains ITU Zones

        """
        return self.get_all(callsign, timestamp)[const.ITUZ]

    def get_country_name(self, callsign, timestamp=timestamp_now):
        """ Returns the country name where the callsign is located

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            str: name of the Country

        Raises:
            KeyError: No Country found for callsign

        Note:
            Don't rely on the country name when working with several instances of
            py:class:`Callinfo`. Clublog and Country-files.org use slightly different names
            for countries. Example:

            - Country-files.com: "Fed. Rep. of Germany"
            - Clublog: "FEDERAL REPUBLIC OF GERMANY"

        """
        return self.get_all(callsign, timestamp)[const.COUNTRY]

    def get_adif_id(self, callsign, timestamp=timestamp_now):
        """ Returns ADIF id of a callsign's country

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            int: containing the country ADIF id

        Raises:
            KeyError: No Country found for callsign

        """
        return self.get_all(callsign, timestamp)[const.ADIF]

    def get_continent(self, callsign, timestamp=timestamp_now):
        """ Returns the continent Identifier of a callsign

        Args:
            callsign (str): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            str: continent identified

        Raises:
            KeyError: No Continent found for callsign

        Note:
            The following continent identifiers are used:

            - EU: Europe
            - NA: North America
            - SA: South America
            - AS: Asia
            - AF: Africa
            - OC: Oceania
            - AN: Antarctica
        """
        return self.get_all(callsign, timestamp)[const.CONTINENT]
