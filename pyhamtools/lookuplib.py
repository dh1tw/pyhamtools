from __future__ import unicode_literals
import os
import logging
import logging.config
import re
import random, string
from datetime import datetime
import xml.etree.ElementTree as ET
import urllib
import json
import copy
import sys
import unicodedata

import requests
from requests.exceptions import ConnectionError, HTTPError, Timeout
from bs4 import BeautifulSoup
import pytz

from . import version
from .consts import LookupConventions as const
from .exceptions import APIKeyMissingError

UTC = pytz.UTC
timestamp_now = datetime.utcnow().replace(tzinfo=UTC)

if sys.version_info < (2, 7,):
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

if sys.version_info.major == 3:
    unicode = str

class LookupLib(object):
    """

    This class is a wrapper for the following three Amateur Radio databases:

    1. Clublog.org (daily updated XML File)
    2. Clublog.org (HTTPS lookup)
    3. Country-files.com (infrequently updated PLIST File)
    4. QRZ.com (HTTP / XML Lookup)

    It's aim is to provide a homogeneous interface to different databases.

    Typically an instance of this class is injected as a dependency in the :py:class:`Callinfo` class, but it can also
    be used directly.

    Even the interface is the same for all lookup sources, the returning data can be different.
    The documentation of the various methods provide more detail.

    By default, LookupLib requires an Internet connection to download the libraries or perform the
    lookup against the Clublog API or QRZ.com.

    The entire lookup data (where database files are downloaded) can also be copied into Redis, which an extremely
    fast in-memory Key/Value store. A LookupLib object can be instanciated to perform then all lookups in Redis,
    instead processing and loading the data from Internet / File. This saves some time and allows several instances
    of :py:class:`LookupLib` to query the same data concurrently.

    Args:
        lookuptype (str) : "clublogxml" or "clublogapi" or "countryfile" or "redis" or "qrz"
        apikey (str): Clublog API Key
        username (str): QRZ.com username
        pwd (str): QRZ.com password
        apiv (str, optional): QRZ.com API Version
        filename (str, optional): Filename for Clublog XML or Country-files.com cty.plist file. When a local file is
        used, no Internet connection not API Key is necessary.
        logger (logging.getLogger(__name__), optional): Python logger
        redis_instance (redis.Redis(), optional): Instance of Redis
        redis_prefix (str, optional): Prefix to identify the lookup data set in Redis


    """
    def __init__(self, lookuptype = "countryfile", apikey=None, apiv="1.3.3", filename=None, logger=None, username=None, pwd=None, redis_instance=None, redis_prefix=None):

        self._logger = None
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger(__name__)
            if sys.version_info[:2] == (2, 6):
                self._logger.addHandler(NullHandler())
            else:
                self._logger.addHandler(logging.NullHandler())

        self._apikey = apikey
        self._apiv = apiv
        self._download = True
        self._lib_filename = filename
        self._redis = redis_instance
        self._redis_prefix = redis_prefix
        self._username = username
        self._pwd = pwd

        if self._lib_filename:
            self._download = False

        self._callsign_exceptions_index = {}
        self._invalid_operations_index = {}
        self._zone_exceptions_index = {}

        self._entities = {}
        self._callsign_exceptions = {}
        self._invalid_operations = {}
        self._zone_exceptions = {}
        self._lookuptype = lookuptype

        if self._lookuptype == "clublogxml":
            self._load_clublogXML(apikey=self._apikey, cty_file=self._lib_filename)
        elif self._lookuptype == "countryfile":
            self._load_countryfile(cty_file=self._lib_filename)
        elif self._lookuptype == "clublogapi":
            pass
        elif self._lookuptype == "redis":
            import redis
        elif self._lookuptype == "qrz":
            self._apikey = self._get_qrz_session_key(self._username, self._pwd)
        else:
            raise AttributeError("Lookup type missing")

    def _get_qrz_session_key(self, username, pwd):

        qrz_api_version = "1.3.3"
        url = "https://xmldata.qrz.com/xml/" + qrz_api_version + "/"
        agent = "PyHamTools"+version.__version__

        params = {"username" : username,
            "password" : pwd,
            "agent" : agent
        }

        if sys.version_info.major == 3:
            encodeurl = url + "?" + urllib.parse.urlencode(params)
        else:
            encodeurl = url + "?" + urllib.urlencode(params)
        response = requests.get(encodeurl, timeout=10)
        doc = BeautifulSoup(response.text, "html.parser")
        session_key = None
        if doc.session.key:
            session_key = doc.session.key.text
        else:
            if doc.session.error:
                raise ValueError(doc.session.error.text)
            else:
                raise ValueError("Could not retrieve Session Key from QRZ.com")

        return session_key


    def copy_data_in_redis(self, redis_prefix, redis_instance):
        """
        Copy the complete lookup data into redis. Old data will be overwritten.

        Args:
            redis_prefix (str): Prefix to distinguish the data in redis for the different looktypes
            redis_instance (str): an Instance of Redis

        Returns:
            bool: returns True when the data has been copied successfully into Redis

        Example:
           Copy the entire lookup data from the Country-files.com PLIST File into Redis. This example requires a running
           instance of Redis, as well the python Redis connector (pip install redis-py).

           >>> from pyhamtools import LookupLib
           >>> import redis
           >>> r = redis.Redis()
           >>> my_lookuplib = LookupLib(lookuptype="countryfile")
           >>> print my_lookuplib.copy_data_in_redis(redis_prefix="CF", redis_instance=r)
           True

           Now let's create an instance of LookupLib, using Redis to query the data

           >>> from pyhamtools import LookupLib
           >>> import redis
           >>> r = redis.Redis()
           >>> my_lookuplib = LookupLib(lookuptype="countryfile", redis_instance=r, redis_prefix="CF")
           >>> my_lookuplib.lookup_callsign("3D2RI")
           {
             u'adif': 460,
             u'continent': u'OC',
             u'country': u'Rotuma Island',
             u'cqz': 32,
             u'ituz': 56,
             u'latitude': -12.48,
             u'longitude': 177.08
           }


        Note:
            This method is available for the following lookup type

            - clublogxml
            - countryfile
        """

        if redis_instance is not None:
            self._redis = redis_instance

        if self._redis is None:
            raise AttributeError("redis_instance is missing")

        if redis_prefix is None:
            raise KeyError("redis_prefix is missing")

        if self._lookuptype == "clublogxml" or self._lookuptype == "countryfile":

            self._push_dict_to_redis(self._entities, redis_prefix, "_entity_")

            self._push_dict_index_to_redis(self._callsign_exceptions_index, redis_prefix, "_call_ex_index_")
            self._push_dict_to_redis(self._callsign_exceptions, redis_prefix, "_call_ex_")

            self._push_dict_index_to_redis(self._prefixes_index, redis_prefix, "_prefix_index_")
            self._push_dict_to_redis(self._prefixes, redis_prefix, "_prefix_")

            self._push_dict_index_to_redis(self._invalid_operations_index, redis_prefix, "_inv_op_index_")
            self._push_dict_to_redis(self._invalid_operations, redis_prefix, "_inv_op_")

            self._push_dict_index_to_redis(self._zone_exceptions_index, redis_prefix, "_zone_ex_index_")
            self._push_dict_to_redis(self._zone_exceptions, redis_prefix, "_zone_ex_")

        return True

    def _push_dict_to_redis(self, push_dict, redis_prefix, name):
        r = self._redis
        for i in push_dict:
            json_data = self._serialize_data(push_dict[i])
            r.delete(redis_prefix + name + str(i))
            r.set(redis_prefix + name + str(i), json_data)
        return True

    def _push_dict_index_to_redis(self, index_dict, redis_prefix, name):
        r = self._redis
        for i in index_dict:
            r.delete(redis_prefix + name + str(i))
            for el in index_dict[i]:
                r.sadd(redis_prefix + name + str(i), el)
        return True



    def lookup_entity(self, entity=None):
        """Returns lookup data of an ADIF Entity

        Args:
            entity (int): ADIF identifier of country

        Returns:
            dict: Dictionary containing the country specific data

        Raises:
            KeyError: No matching entity found

        Example:
           The following code queries the the Clublog XML database for the ADIF entity Turkmenistan, which has
           the id 273.

           >>> from pyhamtools import LookupLib
           >>> my_lookuplib = LookupLib(lookuptype="clublogapi", apikey="myapikey")
           >>> print my_lookuplib.lookup_entity(273)
           {
            'deleted': False,
            'country': u'TURKMENISTAN',
            'longitude': 58.4,
            'cqz': 17,
            'prefix': u'EZ',
            'latitude': 38.0,
            'continent': u'AS'
           }


        Note:
            This method is available for the following lookup type

            - clublogxml
            - redis
            - qrz.com

        """
        if self._lookuptype == "clublogxml":
            entity = int(entity)
            if entity in self._entities:
                return self._strip_metadata(self._entities[entity])
            else:
                raise KeyError

        elif self._lookuptype == "redis":
            if self._redis_prefix is None:
                raise KeyError ("redis_prefix is missing")
            #entity = str(entity)
            json_data = self._redis.get(self._redis_prefix + "_entity_" + str(entity))
            if json_data is not None:
                my_dict = self._deserialize_data(json_data)
                return self._strip_metadata(my_dict)

        elif self._lookuptype == "qrz":
            result = self._lookup_qrz_dxcc(entity, self._apikey)
            return result

        # no matching case
        raise KeyError

    def _strip_metadata(self, my_dict):
        """
        Create a copy of dict and remove not needed data
        """
        new_dict = copy.deepcopy(my_dict)
        if const.START in new_dict:
            del new_dict[const.START]
        if const.END in new_dict:
            del new_dict[const.END]
        if const.WHITELIST in new_dict:
            del new_dict[const.WHITELIST]
        if const.WHITELIST_START in new_dict:
            del new_dict[const.WHITELIST_START]
        if const.WHITELIST_END in new_dict:
            del new_dict[const.WHITELIST_END]
        return new_dict


    def lookup_callsign(self, callsign=None, timestamp=timestamp_now):
        """
        Returns lookup data if an exception exists for a callsign

        Args:
            callsign (string): Amateur radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            dict: Dictionary containing the country specific data of the callsign

        Raises:
            KeyError: No matching callsign found
            APIKeyMissingError: API Key for Clublog missing or incorrect

        Example:
           The following code queries the the online Clublog API for the callsign "VK9XO" on a specific date.

           >>> from pyhamtools import LookupLib
           >>> from datetime import datetime
           >>> import pytz
           >>> my_lookuplib = LookupLib(lookuptype="clublogapi", apikey="myapikey")
           >>> timestamp = datetime(year=1962, month=7, day=7, tzinfo=pytz.UTC)
           >>> print my_lookuplib.lookup_callsign("VK9XO", timestamp)
           {
            'country': u'CHRISTMAS ISLAND',
            'longitude': 105.7,
            'cqz': 29,
            'adif': 35,
            'latitude': -10.5,
            'continent': u'OC'
           }

        Note:
            This method is available for

            - clublogxml
            - clublogapi
            - countryfile
            - qrz.com
            - redis


        """
        callsign = callsign.strip().upper()

        if self._lookuptype == "clublogapi":
            callsign_data =  self._lookup_clublogAPI(callsign=callsign, timestamp=timestamp, apikey=self._apikey)
            if callsign_data[const.ADIF]==1000:
                raise KeyError
            else:
                return callsign_data

        elif self._lookuptype == "clublogxml" or self._lookuptype == "countryfile":

            return self._check_data_for_date(callsign, timestamp, self._callsign_exceptions, self._callsign_exceptions_index)

        elif self._lookuptype == "redis":

            data_dict, index = self._get_dicts_from_redis("_call_ex_", "_call_ex_index_", self._redis_prefix, callsign)
            return self._check_data_for_date(callsign, timestamp, data_dict, index)

        # no matching case
        elif self._lookuptype == "qrz":
            return self._lookup_qrz_callsign(callsign, self._apikey, self._apiv)

        raise KeyError("unknown Callsign")

    def _get_dicts_from_redis(self, name, index_name, redis_prefix, item):
        """
        Retrieve the data of an item from redis and put it in an index and data dictionary to match the
        common query interface.
        """
        r = self._redis
        data_dict = {}
        data_index_dict = {}

        if redis_prefix is None:
            raise KeyError ("redis_prefix is missing")

        if r.scard(redis_prefix + index_name + str(item)) > 0:
            data_index_dict[str(item)] = r.smembers(redis_prefix + index_name + str(item))

            for i in data_index_dict[item]:
                json_data = r.get(redis_prefix + name + str(int(i)))
                data_dict[i] = self._deserialize_data(json_data)

            return (data_dict, data_index_dict)

        raise KeyError ("No Data found in Redis for "+ item)

    def _check_data_for_date(self, item, timestamp, data_dict, data_index_dict):
        """
        Checks if the item is found in the index. An entry in the index points to the data
        in the data_dict. This is mainly used retrieve callsigns and prefixes.
        In case data is found for item, a dict containing the data is returned. Otherwise a KeyError is raised.
        """

        if item in data_index_dict:
            for item in data_index_dict[item]:

                # startdate < timestamp
                if const.START in data_dict[item] and not const.END in data_dict[item]:
                    if data_dict[item][const.START] < timestamp:
                        item_data = copy.deepcopy(data_dict[item])
                        del item_data[const.START]
                        return item_data

                # enddate > timestamp
                elif not const.START in data_dict[item] and const.END in data_dict[item]:
                    if data_dict[item][const.END] > timestamp:
                        item_data = copy.deepcopy(data_dict[item])
                        del item_data[const.END]
                        return item_data

                # startdate > timestamp > enddate
                elif const.START in data_dict[item] and const.END in data_dict[item]:
                    if data_dict[item][const.START] < timestamp \
                            and data_dict[item][const.END] > timestamp:
                        item_data = copy.deepcopy(data_dict[item])
                        del item_data[const.START]
                        del item_data[const.END]
                        return item_data

                # no startdate or enddate available
                elif not const.START in data_dict[item] and not const.END in data_dict[item]:
                    return data_dict[item]

        raise KeyError


    def _check_inv_operation_for_date(self, item, timestamp, data_dict, data_index_dict):
        """
        Checks if the callsign is marked as an invalid operation for a given timestamp.
        In case the operation is invalid, True is returned. Otherwise a KeyError is raised.
        """

        if item in data_index_dict:
            for item in data_index_dict[item]:

                # startdate < timestamp
                if const.START in data_dict[item] and not const.END in data_dict[item]:
                    if data_dict[item][const.START] < timestamp:
                        return True

                # enddate > timestamp
                elif not const.START in data_dict[item] and const.END in data_dict[item]:
                    if data_dict[item][const.END] > timestamp:
                        return True

                # startdate > timestamp > enddate
                elif const.START in data_dict[item] and const.END in data_dict[item]:
                    if data_dict[item][const.START] < timestamp \
                            and data_dict[item][const.END] > timestamp:
                        return True

                # no startdate or enddate available
                elif not const.START in data_dict[item] and not const.END in data_dict[item]:
                    return True

        raise KeyError


    def lookup_prefix(self, prefix, timestamp=timestamp_now):
        """
        Returns lookup data of a Prefix

        Args:
            prefix (string): Prefix of a Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            dict: Dictionary containing the country specific data of the Prefix

        Raises:
            KeyError: No matching Prefix found
            APIKeyMissingError: API Key for Clublog missing or incorrect

        Example:
           The following code shows how to obtain the information for the prefix "DH" from the countryfile.com
           database (default database).

           >>> from pyhamtools import LookupLib
           >>> myLookupLib = LookupLib()
           >>> print myLookupLib.lookup_prefix("DH")
           {
            'adif': 230,
            'country': u'Fed. Rep. of Germany',
            'longitude': 10.0,
            'cqz': 14,
            'ituz': 28,
            'latitude': 51.0,
            'continent': u'EU'
           }

        Note:
            This method is available for

            - clublogxml
            - countryfile
            - redis

        """

        prefix = prefix.strip().upper()

        if self._lookuptype == "clublogxml" or self._lookuptype == "countryfile":

            return self._check_data_for_date(prefix, timestamp, self._prefixes, self._prefixes_index)

        elif self._lookuptype == "redis":

            data_dict, index = self._get_dicts_from_redis("_prefix_", "_prefix_index_", self._redis_prefix, prefix)
            return self._check_data_for_date(prefix, timestamp, data_dict, index)

        # no matching case
        raise KeyError

    def is_invalid_operation(self, callsign, timestamp=datetime.utcnow().replace(tzinfo=UTC)):
        """
        Returns True if an operations is known as invalid

        Args:
            callsign (string): Amateur Radio callsign
            timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            bool: True if a record exists for this callsign (at the given time)

        Raises:
            KeyError: No matching callsign found
            APIKeyMissingError: API Key for Clublog missing or incorrect

        Example:
           The following code checks the Clublog XML database if the operation is valid for two dates.

           >>> from pyhamtools import LookupLib
           >>> from datetime import datetime
           >>> import pytz
           >>> my_lookuplib = LookupLib(lookuptype="clublogxml", apikey="myapikey")
           >>> print my_lookuplib.is_invalid_operation("5W1CFN")
           True
           >>> try:
           >>>   timestamp = datetime(year=2012, month=1, day=31).replace(tzinfo=pytz.UTC)
           >>>   my_lookuplib.is_invalid_operation("5W1CFN", timestamp)
           >>> except KeyError:
           >>>   print "Seems to be invalid operation before 31.1.2012"
           Seems to be an invalid operation before 31.1.2012

        Note:
            This method is available for

            - clublogxml
            - redis

        """

        callsign = callsign.strip().upper()

        if self._lookuptype == "clublogxml":

            return self._check_inv_operation_for_date(callsign, timestamp, self._invalid_operations, self._invalid_operations_index)

        elif self._lookuptype == "redis":

            data_dict, index = self._get_dicts_from_redis("_inv_op_", "_inv_op_index_", self._redis_prefix, callsign)
            return self._check_inv_operation_for_date(callsign, timestamp, data_dict, index)

        #no matching case
        raise KeyError


    def _check_zone_exception_for_date(self, item, timestamp, data_dict, data_index_dict):
        """
        Checks the index and data if a cq-zone exception exists for the callsign
        When a zone exception is found, the zone is returned. If no exception is found
        a KeyError is raised

        """
        if item in data_index_dict:
            for item in data_index_dict[item]:

                # startdate < timestamp
                if const.START in data_dict[item] and not const.END in data_dict[item]:
                    if data_dict[item][const.START] < timestamp:
                        return data_dict[item][const.CQZ]

                # enddate > timestamp
                elif not const.START in data_dict[item] and const.END in data_dict[item]:
                    if data_dict[item][const.END] > timestamp:
                        return data_dict[item][const.CQZ]

                # startdate > timestamp > enddate
                elif const.START in data_dict[item] and const.END in data_dict[item]:
                    if data_dict[item][const.START] < timestamp \
                            and data_dict[item][const.END] > timestamp:
                        return data_dict[item][const.CQZ]

                # no startdate or enddate available
                elif not const.START in data_dict[item] and not const.END in data_dict[item]:
                        return data_dict[item][const.CQZ]

        raise KeyError


    def lookup_zone_exception(self, callsign, timestamp=datetime.utcnow().replace(tzinfo=UTC)):
        """
        Returns a CQ Zone if an exception exists for the given callsign

        Args:
        callsign (string): Amateur radio callsign
        timestamp (datetime, optional): datetime in UTC (tzinfo=pytz.UTC)

        Returns:
            int: Value of the the CQ Zone exception which exists for this callsign (at the given time)

        Raises:
            KeyError: No matching callsign found
            APIKeyMissingError: API Key for Clublog missing or incorrect

        Example:
           The following code checks the Clublog XML database if a CQ Zone exception exists for the callsign DP0GVN.

           >>> from pyhamtools import LookupLib
           >>> my_lookuplib = LookupLib(lookuptype="clublogxml", apikey="myapikey")
           >>> print my_lookuplib.lookup_zone_exception("DP0GVN")
           38

           The prefix "DP" It is assigned to Germany, but the station is located in Antarctica, and therefore
           in CQ Zone 38

        Note:
            This method is available for

            - clublogxml
            - redis

        """

        callsign = callsign.strip().upper()

        if self._lookuptype == "clublogxml":

            return self._check_zone_exception_for_date(callsign, timestamp, self._zone_exceptions, self._zone_exceptions_index)

        elif self._lookuptype == "redis":

            data_dict, index = self._get_dicts_from_redis("_zone_ex_", "_zone_ex_index_", self._redis_prefix, callsign)
            return self._check_zone_exception_for_date(callsign, timestamp, data_dict, index)

        #no matching case
        raise KeyError

    def _lookup_clublogAPI(self, callsign=None, timestamp=timestamp_now, url="https://secure.clublog.org/dxcc", apikey=None):
        """ Set up the Lookup object for Clublog Online API
        """

        params = {"year" : timestamp.strftime("%Y"),
            "month" : timestamp.strftime("%m"),
            "day" : timestamp.strftime("%d"),
            "hour" : timestamp.strftime("%H"),
            "minute" : timestamp.strftime("%M"),
            "api" : apikey,
            "full" : "1",
            "call" : callsign
        }

        if sys.version_info.major == 3:
            encodeurl = url + "?" + urllib.parse.urlencode(params)
        else:
            encodeurl = url + "?" + urllib.urlencode(params)
        response = requests.get(encodeurl, timeout=5)

        if not self._check_html_response(response):
            raise LookupError

        jsonLookup = response.json()
        lookup = {}

        for item in jsonLookup:
            if item == "Name": lookup[const.COUNTRY] = jsonLookup["Name"]
            elif item == "DXCC": lookup[const.ADIF] = int(jsonLookup["DXCC"])
            elif item == "Lon": lookup[const.LONGITUDE] = float(jsonLookup["Lon"])*(-1)
            elif item == "Lat": lookup[const.LATITUDE] = float(jsonLookup["Lat"])
            elif item == "CQZ": lookup[const.CQZ] = int(jsonLookup["CQZ"])
            elif item == "Continent": lookup[const.CONTINENT] = jsonLookup["Continent"]

        if lookup[const.ADIF] == 0:
            raise KeyError
        else:
            return lookup

    def _request_callsign_info_from_qrz(self, callsign, apikey, apiv="1.3.3"):
        qrz_api_version = apiv
        url = "https://xmldata.qrz.com/xml/" + qrz_api_version + "/"

        params = {
            "s": apikey,
            "callsign" : callsign,
        }

        if sys.version_info.major == 3:
            encodeurl = url + "?" + urllib.parse.urlencode(params)
        else:
            encodeurl = url + "?" + urllib.urlencode(params)
        response = requests.get(encodeurl, timeout=5)
        return response

    def _request_dxcc_info_from_qrz(self, dxcc_or_callsign, apikey, apiv="1.3.3"):
        qrz_api_version = apiv
        url = "https://xmldata.qrz.com/xml/" + qrz_api_version + "/"

        params = {
            "s": apikey,
            "dxcc" : str(dxcc_or_callsign),
        }

        if sys.version_info.major == 3:
            encodeurl = url + "?" + urllib.parse.urlencode(params)
        else:
            encodeurl = url + "?" + urllib.urlencode(params)
        response = requests.get(encodeurl, timeout=5)
        return response

    def _lookup_qrz_dxcc(self, dxcc_or_callsign, apikey, apiv="1.3.3"):
        """ Performs the dxcc lookup against the QRZ.com XML API:
        """

        response = self._request_dxcc_info_from_qrz(dxcc_or_callsign, apikey, apiv=apiv)

        root = BeautifulSoup(response.text, "html.parser")
        lookup = {}

        if root.error: #try to get a new session key and try to request again

            if re.search('No DXCC Information for', root.error.text, re.I):  #No data available for callsign
                raise KeyError(root.error.text)
            elif re.search('Session Timeout', root.error.text, re.I): # Get new session key
                self._apikey = apikey = self._get_qrz_session_key(self._username, self._pwd)
                response = self._request_dxcc_info_from_qrz(dxcc_or_callsign, apikey)
                root = BeautifulSoup(response.text, "html.parser")
            else:
                raise AttributeError("Session Key Missing") #most likely session key missing or invalid

        if root.dxcc is None:
            raise ValueError

        if root.dxcc.dxcc:
            lookup[const.ADIF] = int(root.dxcc.dxcc.text)
        if root.dxcc.cc:
            lookup['cc'] = root.dxcc.cc.text
        if root.dxcc.cc:
            lookup['ccc'] = root.dxcc.ccc.text
        if root.find('name'):
            lookup[const.COUNTRY] = root.find('name').get_text()
        if root.dxcc.continent:
            lookup[const.CONTINENT] = root.dxcc.continent.text
        if root.dxcc.ituzone:
            lookup[const.ITUZ] = int(root.dxcc.ituzone.text)
        if root.dxcc.cqzone:
            lookup[const.CQZ] = int(root.dxcc.cqzone.text)
        if root.dxcc.timezone:
            lookup['timezone'] = float(root.dxcc.timezone.text)
        if root.dxcc.lat:
            lookup[const.LATITUDE] = float(root.dxcc.lat.text)
        if root.dxcc.lon:
            lookup[const.LONGITUDE] = float(root.dxcc.lon.text)

        return lookup


    def _lookup_qrz_callsign(self, callsign=None, apikey=None, apiv="1.3.3"):
        """ Performs the callsign lookup against the QRZ.com XML API:
        """

        if apikey is None:
            raise AttributeError("Session Key Missing")

        callsign = callsign.upper()

        response = self._request_callsign_info_from_qrz(callsign, apikey, apiv)

        root = BeautifulSoup(response.text, "html.parser")
        lookup = {}

        if root.error:

            if re.search('Not found', root.error.text, re.I):  #No data available for callsign
                raise KeyError(root.error.text)

            #try to get a new session key and try to request again
            elif re.search('Session Timeout', root.error.text, re.I) or re.search('Invalid session key', root.error.text, re.I):
                apikey = self._get_qrz_session_key(self._username, self._pwd)
                response = self._request_callsign_info_from_qrz(callsign, apikey, apiv)
                root = BeautifulSoup(response.text, "html.parser")

                #if this fails again, raise error
                if root.error:

                    if re.search('Not found', root.error.text, re.I):  #No data available for callsign
                        raise KeyError(root.error.text)
                    else:
                        raise AttributeError(root.error.text) #most likely session key invalid
                else:
                    #update API Key ob Lookup object
                    self._apikey = apikey

            else:
                raise AttributeError(root.error.text) #most likely session key missing

        if root.callsign is None:
            raise ValueError

        if root.callsign.call:
            lookup[const.CALLSIGN] = root.callsign.call.text
        if root.callsign.xref:
            lookup[const.XREF] = root.callsign.xref.text
        if root.callsign.aliases:
            lookup[const.ALIASES] = root.callsign.aliases.text.split(',')
        if root.callsign.dxcc:
            lookup[const.ADIF] = int(root.callsign.dxcc.text)
        if root.callsign.fname:
            lookup[const.FNAME] = root.callsign.fname.text
        if root.callsign.find("name"):
            lookup[const.NAME] = root.callsign.find('name').get_text()
        if root.callsign.addr1:
            lookup[const.ADDR1] = root.callsign.addr1.text
        if root.callsign.addr2:
            lookup[const.ADDR2] = root.callsign.addr2.text
        if root.callsign.state:
            lookup[const.STATE] = root.callsign.state.text
        if root.callsign.zip:
            lookup[const.ZIPCODE] = root.callsign.zip.text
        if root.callsign.country:
            lookup[const.COUNTRY] = root.callsign.country.text
        if root.callsign.ccode:
            lookup[const.CCODE] = int(root.callsign.ccode.text)
        if root.callsign.lat:
            lookup[const.LATITUDE] = float(root.callsign.lat.text)
        if root.callsign.lon:
            lookup[const.LONGITUDE] = float(root.callsign.lon.text)
        if root.callsign.grid:
            lookup[const.LOCATOR] = root.callsign.grid.text
        if root.callsign.county:
            lookup[const.COUNTY] = root.callsign.county.text
        if root.callsign.fips:
            lookup[const.FIPS] = int(root.callsign.fips.text) # check type
        if root.callsign.land:
            lookup[const.LAND] = root.callsign.land.text
        if root.callsign.efdate:
            try:
                lookup[const.EFDATE] = datetime.strptime(root.callsign.efdate.text, '%Y-%m-%d').replace(tzinfo=UTC)
            except ValueError:
                self._logger.debug("[QRZ.com] efdate: Invalid DateTime; " + callsign + " " + root.callsign.efdate.text)
        if root.callsign.expdate:
            try:
                lookup[const.EXPDATE] = datetime.strptime(root.callsign.expdate.text, '%Y-%m-%d').replace(tzinfo=UTC)
            except ValueError:
                self._logger.debug("[QRZ.com] expdate: Invalid DateTime; " + callsign + " " + root.callsign.expdate.text)
        if root.callsign.p_call:
            lookup[const.P_CALL] = root.callsign.p_call.text
        if root.callsign.find('class'):
             lookup[const.LICENSE_CLASS] = root.callsign.find('class').get_text()
        if root.callsign.codes:
            lookup[const.CODES] = root.callsign.codes.text
        if root.callsign.qslmgr:
            lookup[const.QSLMGR] = root.callsign.qslmgr.text
        if root.callsign.email:
            lookup[const.EMAIL] = root.callsign.email.text
        if root.callsign.url:
            lookup[const.URL] = root.callsign.url.text
        if root.callsign.u_views:
            lookup[const.U_VIEWS] = int(root.callsign.u_views.text)
        if root.callsign.bio:
            lookup[const.BIO] = root.callsign.bio.text
        if root.callsign.biodate:
            try:
                lookup[const.BIODATE] = datetime.strptime(root.callsign.biodate.text, '%Y-%m-%d %H:%M:%S').replace(tzinfo=UTC)
            except ValueError:
                self._logger.warning("[QRZ.com] biodate: Invalid DateTime; " + callsign)
        if root.callsign.image:
            lookup[const.IMAGE] = root.callsign.image.text
        if root.callsign.imageinfo:
            lookup[const.IMAGE_INFO] = root.callsign.imageinfo.text
        if root.callsign.serial:
            lookup[const.SERIAL] = long(root.callsign.serial.text)
        if root.callsign.moddate:
            try:
                lookup[const.MODDATE] = datetime.strptime(root.callsign.moddate.text, '%Y-%m-%d %H:%M:%S').replace(tzinfo=UTC)
            except ValueError:
                self._logger.warning("[QRZ.com] moddate: Invalid DateTime; " + callsign)
        if root.callsign.MSA:
            lookup[const.MSA] = int(root.callsign.MSA.text)
        if root.callsign.AreaCode:
            lookup[const.AREACODE] = int(root.callsign.AreaCode.text)
        if root.callsign.TimeZone:
            lookup[const.TIMEZONE] = int(root.callsign.TimeZone.text)
        if root.callsign.GMTOffset:
            lookup[const.GMTOFFSET] = float(root.callsign.GMTOffset.text)
        if root.callsign.DST:
            if root.callsign.DST.text == "Y":
                lookup[const.DST] = True
            else:
                lookup[const.DST] = False
        if root.callsign.eqsl:
            if root.callsign.eqsl.text == "1":
                lookup[const.EQSL] = True
            else:
                lookup[const.EQSL] = False
        if root.callsign.mqsl:
            if root.callsign.mqsl.text == "1":
                lookup[const.MQSL] = True
            else:
                lookup[const.MQSL] = False
        if root.callsign.cqzone:
            lookup[const.CQZ] = int(root.callsign.cqzone.text)
        if root.callsign.ituzone:
            lookup[const.ITUZ] = int(root.callsign.ituzone.text)
        if root.callsign.born:
            lookup[const.BORN] = int(root.callsign.born.text)
        if root.callsign.user:
            lookup[const.USER_MGR] = root.callsign.user.text
        if root.callsign.lotw:
            if root.callsign.lotw.text == "1":
                lookup[const.LOTW] = True
            else:
                lookup[const.LOTW] = False
        if root.callsign.iota:
            lookup[const.IOTA] = root.callsign.iota.text
        if root.callsign.geoloc:
            lookup[const.GEOLOC] = root.callsign.geoloc.text

        # if sys.version_info >= (2,):
        #     for item in lookup:
        #         if isinstance(lookup[item], unicode):
        #             print item, repr(lookup[item])
        return lookup

    def _load_clublogXML(self,
                        url="https://secure.clublog.org/cty.php",
                        apikey=None,
                        cty_file=None):
        """ Load and process the ClublogXML file either as a download or from file
        """

        if self._download:
            cty_file = self._download_file(
                    url = url,
                    apikey = apikey)
        else:
            cty_file = self._lib_filename

        header = self._extract_clublog_header(cty_file)
        cty_file = self._remove_clublog_xml_header(cty_file)
        cty_dict = self._parse_clublog_xml(cty_file)

        self._entities = cty_dict["entities"]
        self._callsign_exceptions = cty_dict["call_exceptions"]
        self._prefixes = cty_dict["prefixes"]
        self._invalid_operations = cty_dict["invalid_operations"]
        self._zone_exceptions = cty_dict["zone_exceptions"]

        self._callsign_exceptions_index = cty_dict["call_exceptions_index"]
        self._prefixes_index = cty_dict["prefixes_index"]
        self._invalid_operations_index = cty_dict["invalid_operations_index"]
        self._zone_exceptions_index = cty_dict["zone_exceptions_index"]

        return True

    def _load_countryfile(self,
                         url="https://www.country-files.com/cty/cty.plist",
                         country_mapping_filename="countryfilemapping.json",
                         cty_file=None):
        """ Load and process the ClublogXML file either as a download or from file
        """

        cwdFile = os.path.abspath(os.path.join(os.getcwd(), country_mapping_filename))
        pkgFile = os.path.abspath(os.path.join(os.path.dirname(__file__), country_mapping_filename))

        # from cwd
        if os.path.exists(cwdFile):
            # country mapping files contains the ADIF identifiers of a particular
            # country since the country-files do not provide this information (only DXCC id)
            country_mapping_filename = cwdFile
        # from package
        elif os.path.exists(pkgFile):
            country_mapping_filename = pkgFile
        else:
            country_mapping_filename = None

        if self._download:
            cty_file = self._download_file(url=url)
        else:
            cty_file = os.path.abspath(cty_file)

        cty_dict = self._parse_country_file(cty_file, country_mapping_filename)
        self._callsign_exceptions = cty_dict["exceptions"]
        self._prefixes = cty_dict["prefixes"]
        self._callsign_exceptions_index = cty_dict["exceptions_index"]
        self._prefixes_index = cty_dict["prefixes_index"]

        return True

    def _download_file(self, url, apikey=None):
        """ Download lookup files either from Clublog or Country-files.com
        """
        import gzip
        import tempfile

        cty = {}
        cty_date = ""
        cty_file_path = None

        filename = None

        # download file
        if apikey: # clublog
            response = requests.get(url+"?api="+apikey, timeout=10)
        else: # country-files.com
            response = requests.get(url, timeout=10)

        if not self._check_html_response(response):
            raise LookupError

        #Clublog Webserver Header
        if "Content-Disposition" in response.headers:
            f = re.search('filename=".+"', response.headers["Content-Disposition"])
            if f:
                f = f.group(0)
                filename = re.search('".+"', f).group(0).replace('"', '')

        #Country-files.org webserver header
        else:
            f = re.search('/.{4}plist$', url)
            if f:
                f = f.group(0)
                filename = f[1:]

        if not filename:
            filename = "cty_" + self._generate_random_word(5)

        download_file_path = os.path.join(tempfile.gettempdir(), filename)
        with open(download_file_path, "wb") as download_file:
            download_file.write(response.content)
        self._logger.debug(str(download_file_path) + " successfully downloaded")

        # unzip file, if gz
        if os.path.splitext(download_file_path)[1][1:] == "gz":

            download_file = gzip.open(download_file_path, "r")
            try:
                cty_file_path = os.path.join(os.path.splitext(download_file_path)[0])
                with open(cty_file_path, "wb") as cty_file:
                    cty_file.write(download_file.read())
                self._logger.debug(str(cty_file_path) + " successfully extracted")
            finally:
                download_file.close()
        else:
            cty_file_path = download_file_path

        return cty_file_path

    def _extract_clublog_header(self, cty_xml_filename):
        """
        Extract the header of the Clublog XML File
        """

        cty_header = {}

        try:
            with open(cty_xml_filename, "r") as cty:
                raw_header = cty.readline()

            cty_date = re.search("date='.+'", raw_header)
            if cty_date:
                cty_date = cty_date.group(0).replace("date=", "").replace("'", "")
                cty_date = datetime.strptime(cty_date[:19], '%Y-%m-%dT%H:%M:%S')
                cty_date.replace(tzinfo=UTC)
                cty_header["Date"] = cty_date

            cty_ns = re.search("xmlns='.+[']", raw_header)
            if cty_ns:
                cty_ns = cty_ns.group(0).replace("xmlns=", "").replace("'", "")
                cty_header['NameSpace'] = cty_ns

            if len(cty_header) == 2:
                self._logger.debug("Header successfully retrieved from CTY File")
            elif len(cty_header) < 2:
                self._logger.warning("Header could only be partically retrieved from CTY File")
                self._logger.warning("Content of Header: ")
                for key in cty_header:
                    self._logger.warning(str(key)+": "+str(cty_header[key]))
            return cty_header

        except Exception as e:
            self._logger.error("Clublog CTY File could not be opened / modified")
            self._logger.error("Error Message: " + str(e))
            return


    def _remove_clublog_xml_header(self, cty_xml_filename):
        """
            remove the header of the Clublog XML File to make it
            properly parseable for the python ElementTree XML parser
        """
        import tempfile

        try:
            with open(cty_xml_filename, "r") as f:
                content = f.readlines()

            cty_dir = tempfile.gettempdir()
            cty_name = os.path.split(cty_xml_filename)[1]
            cty_xml_filename_no_header = os.path.join(cty_dir, "NoHeader_"+cty_name)

            with open(cty_xml_filename_no_header, "w") as f:
                f.writelines("<clublog>\n\r")
                f.writelines(content[1:])

            self._logger.debug("Header successfully modified for XML Parsing")
            return cty_xml_filename_no_header

        except Exception as e:
            self._logger.error("Clublog CTY could not be opened / modified")
            self._logger.error("Error Message: " + str(e))
            return

    def _parse_clublog_xml(self, cty_xml_filename):
        """
        parse the content of a clublog XML file and return the
        parsed values in dictionaries

        """

        entities = {}
        call_exceptions = {}
        prefixes = {}
        invalid_operations = {}
        zone_exceptions = {}

        call_exceptions_index = {}
        prefixes_index = {}
        invalid_operations_index = {}
        zone_exceptions_index = {}

        cty_tree = ET.parse(cty_xml_filename)
        root = cty_tree.getroot()

        #retrieve ADIF Country Entities
        cty_entities = cty_tree.find("entities")
        self._logger.debug("total entities: " + str(len(cty_entities)))
        if len(cty_entities) > 1:
            for cty_entity in cty_entities:
                try:
                    entity = {}
                    for item in cty_entity:
                        if item.tag == "name":
                            entity[const.COUNTRY] = unicode(item.text)
                            self._logger.debug(unicode(item.text))
                        elif item.tag == "prefix":
                            entity[const.PREFIX] = unicode(item.text)
                        elif item.tag == "deleted":
                            if item.text == "TRUE":
                                entity[const.DELETED] = True
                            else:
                                entity[const.DELETED] = False
                        elif item.tag == "cqz":
                            entity[const.CQZ] = int(item.text)
                        elif item.tag == "cont":
                            entity[const.CONTINENT] = unicode(item.text)
                        elif item.tag == "long":
                            entity[const.LONGITUDE] = float(item.text)
                        elif item.tag == "lat":
                            entity[const.LATITUDE] = float(item.text)
                        elif item.tag == "start":
                            dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                            entity[const.START] = dt.replace(tzinfo=UTC)
                        elif item.tag == "end":
                            dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                            entity[const.END] = dt.replace(tzinfo=UTC)
                        elif item.tag == "whitelist":
                            if item.text == "TRUE":
                                entity[const.WHITELIST] = True
                            else:
                                entity[const.WHITELIST] = False
                        elif item.tag == "whitelist_start":
                            dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                            entity[const.WHITELIST_START] = dt.replace(tzinfo=UTC)
                        elif item.tag == "whitelist_end":
                            dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                            entity[const.WHITELIST_END] = dt.replace(tzinfo=UTC)
                except AttributeError:
                    self._logger.error("Error while processing: ")
                entities[int(cty_entity[0].text)] = entity
            self._logger.debug(str(len(entities))+" Entities added")
        else:
            raise Exception("No Country Entities detected in XML File")


        cty_exceptions = cty_tree.find("exceptions")
        if len(cty_exceptions) > 1:
            for cty_exception in cty_exceptions:
                call_exception = {}
                for item in cty_exception:
                    if item.tag == "call":
                        call = str(item.text)
                        if call in call_exceptions_index.keys():
                            call_exceptions_index[call].append(int(cty_exception.attrib["record"]))
                        else:
                            call_exceptions_index[call] = [int(cty_exception.attrib["record"])]
                    elif item.tag == "entity":
                        call_exception[const.COUNTRY] = unicode(item.text)
                    elif item.tag == "adif":
                        call_exception[const.ADIF] = int(item.text)
                    elif item.tag == "cqz":
                        call_exception[const.CQZ] = int(item.text)
                    elif item.tag == "cont":
                        call_exception[const.CONTINENT] = unicode(item.text)
                    elif item.tag == "long":
                        call_exception[const.LONGITUDE] = float(item.text)
                    elif item.tag == "lat":
                        call_exception[const.LATITUDE] = float(item.text)
                    elif item.tag == "start":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        call_exception[const.START] = dt.replace(tzinfo=UTC)
                    elif item.tag == "end":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        call_exception[const.END] = dt.replace(tzinfo=UTC)
                    call_exceptions[int(cty_exception.attrib["record"])] = call_exception

            self._logger.debug(str(len(call_exceptions))+" Exceptions added")
            self._logger.debug(str(len(call_exceptions_index))+" unique Calls in Index ")

        else:
            raise Exception("No Exceptions detected in XML File")


        cty_prefixes = cty_tree.find("prefixes")
        if len(cty_prefixes) > 1:
            for cty_prefix in cty_prefixes:
                prefix = {}
                for item in cty_prefix:
                    pref = None
                    if item.tag == "call":

                        #create index for this prefix
                        call = str(item.text)
                        if call in prefixes_index.keys():
                            prefixes_index[call].append(int(cty_prefix.attrib["record"]))
                        else:
                            prefixes_index[call] = [int(cty_prefix.attrib["record"])]
                    if item.tag == "entity":
                        prefix[const.COUNTRY] = unicode(item.text)
                    elif item.tag == "adif":
                        prefix[const.ADIF] = int(item.text)
                    elif item.tag == "cqz":
                        prefix[const.CQZ] = int(item.text)
                    elif item.tag == "cont":
                        prefix[const.CONTINENT] = unicode(item.text)
                    elif item.tag == "long":
                        prefix[const.LONGITUDE] = float(item.text)
                    elif item.tag == "lat":
                        prefix[const.LATITUDE] = float(item.text)
                    elif item.tag == "start":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        prefix[const.START] = dt.replace(tzinfo=UTC)
                    elif item.tag == "end":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        prefix[const.END] = dt.replace(tzinfo=UTC)
                    prefixes[int(cty_prefix.attrib["record"])] = prefix

            self._logger.debug(str(len(prefixes))+" Prefixes added")
            self._logger.debug(str(len(prefixes_index))+" unique Prefixes in Index")
        else:
            raise Exception("No Prefixes detected in XML File")

        cty_inv_operations = cty_tree.find("invalid_operations")
        if len(cty_inv_operations) > 1:
            for cty_inv_operation in cty_inv_operations:
                invalid_operation = {}
                for item in cty_inv_operation:
                    call = None
                    if item.tag == "call":
                        call = str(item.text)
                        if call in invalid_operations_index.keys():
                            invalid_operations_index[call].append(int(cty_inv_operation.attrib["record"]))
                        else:
                            invalid_operations_index[call] = [int(cty_inv_operation.attrib["record"])]

                    elif item.tag == "start":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        invalid_operation[const.START] = dt.replace(tzinfo=UTC)
                    elif item.tag == "end":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        invalid_operation[const.END] = dt.replace(tzinfo=UTC)
                    invalid_operations[int(cty_inv_operation.attrib["record"])] = invalid_operation

            self._logger.debug(str(len(invalid_operations))+" Invalid Operations added")
            self._logger.debug(str(len(invalid_operations_index))+" unique Calls in Index")
        else:
            raise Exception("No records for invalid operations detected in XML File")


        cty_zone_exceptions = cty_tree.find("zone_exceptions")
        if len(cty_zone_exceptions) > 1:
            for cty_zone_exception in cty_zone_exceptions:
                zoneException = {}
                for item in cty_zone_exception:
                    call = None
                    if item.tag == "call":
                        call = str(item.text)
                        if call in zone_exceptions_index.keys():
                            zone_exceptions_index[call].append(int(cty_zone_exception.attrib["record"]))
                        else:
                            zone_exceptions_index[call] = [int(cty_zone_exception.attrib["record"])]

                    elif item.tag == "zone":
                        zoneException[const.CQZ] = int(item.text)
                    elif item.tag == "start":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        zoneException[const.START] = dt.replace(tzinfo=UTC)
                    elif item.tag == "end":
                        dt = datetime.strptime(item.text[:19], '%Y-%m-%dT%H:%M:%S')
                        zoneException[const.END] = dt.replace(tzinfo=UTC)
                    zone_exceptions[int(cty_zone_exception.attrib["record"])] = zoneException

            self._logger.debug(str(len(zone_exceptions))+" Zone Exceptions added")
            self._logger.debug(str(len(zone_exceptions_index))+" unique Calls in Index")
        else:
            raise Exception("No records for zone exceptions detected in XML File")

        result = {
            "entities" : entities,
            "call_exceptions" : call_exceptions,
            "prefixes" : prefixes,
            "invalid_operations" : invalid_operations,
            "zone_exceptions" : zone_exceptions,
            "prefixes_index" : prefixes_index,
            "call_exceptions_index" : call_exceptions_index,
            "invalid_operations_index" : invalid_operations_index,
            "zone_exceptions_index" : zone_exceptions_index,
        }
        return result

    def _parse_country_file(self, cty_file, country_mapping_filename=None):
        """
        Parse the content of a PLIST file from country-files.com return the
        parsed values in dictionaries.
        Country-files.com provides Prefixes and Exceptions

        """

        import plistlib

        cty_list = None
        entities = {}
        exceptions = {}
        prefixes = {}

        exceptions_index = {}
        prefixes_index = {}

        exceptions_counter = 0
        prefixes_counter = 0

        mapping = None

        with open(country_mapping_filename, "r") as f:
            mapping = json.loads(f.read(),encoding='UTF-8')

        cty_list = plistlib.readPlist(cty_file)

        for item in cty_list:
            entry = {}
            call = str(item)
            entry[const.COUNTRY] = unicode(cty_list[item]["Country"])
            if mapping:
                 entry[const.ADIF] = int(mapping[cty_list[item]["Country"]])
            entry[const.CQZ] = int(cty_list[item]["CQZone"])
            entry[const.ITUZ] = int(cty_list[item]["ITUZone"])
            entry[const.CONTINENT] = unicode(cty_list[item]["Continent"])
            entry[const.LATITUDE] = float(cty_list[item]["Latitude"])
            entry[const.LONGITUDE] = float(cty_list[item]["Longitude"])*(-1)

            if cty_list[item]["ExactCallsign"]:
                if call in exceptions_index.keys():
                    exceptions_index[call].append(exceptions_counter)
                else:
                    exceptions_index[call] = [exceptions_counter]
                exceptions[exceptions_counter] = entry
                exceptions_counter += 1
            else:
                if call in prefixes_index.keys():
                    prefixes_index[call].append(prefixes_counter)
                else:
                    prefixes_index[call] = [prefixes_counter]
                prefixes[prefixes_counter] = entry
                prefixes_counter += 1

        self._logger.debug(str(len(prefixes))+" Prefixes added")
        self._logger.debug(str(len(prefixes_index))+" Prefixes in Index")
        self._logger.debug(str(len(exceptions))+" Exceptions added")
        self._logger.debug(str(len(exceptions_index))+" Exceptions in Index")

        result = {
            "prefixes" : prefixes,
            "exceptions" : exceptions,
            "prefixes_index" : prefixes_index,
            "exceptions_index" : exceptions_index,
        }

        return result

    def _generate_random_word(self, length):
        """
            Generates a random word
        """
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

    def _check_html_response(self, response):
        """
            Checks if the API Key is valid and if the request returned a 200 status (ok)
        """

        error1 = "Access to this form requires a valid API key. For more info see: http://www.clublog.org/need_api.php"
        error2 = "Invalid or missing API Key"

        if response.status_code == requests.codes.ok:
            return True
        else:
            err_str = "HTTP Status Code: " + str(response.status_code) + " HTTP Response: " + str(response.text)
            self._logger.error(err_str)
            if response.status_code == 403:
                raise APIKeyMissingError
            else:
                raise LookupError(err_str)


    def _serialize_data(self, my_dict):
        """
        Serialize a Dictionary into JSON
        """
        new_dict = {}
        for item in my_dict:
            if isinstance(my_dict[item], datetime):
                new_dict[item] = my_dict[item].strftime('%Y-%m-%d%H:%M:%S')
            else:
                new_dict[item] = str(my_dict[item])

        return json.dumps(new_dict)

    def _deserialize_data(self, json_data):
        """
        Deserialize a JSON into a dictionary
        """

        my_dict = json.loads(json_data.decode('utf8').replace("'", '"'),
            encoding='UTF-8')

        for item in my_dict:
            if item == const.ADIF:
                my_dict[item] = int(my_dict[item])
            elif item == const.DELETED:
                my_dict[item] = self._str_to_bool(my_dict[item])
            elif item == const.CQZ:
                my_dict[item] = int(my_dict[item])
            elif item == const.ITUZ:
                my_dict[item] = int(my_dict[item])
            elif item == const.LATITUDE:
                my_dict[item] = float(my_dict[item])
            elif item == const.LONGITUDE:
                my_dict[item] = float(my_dict[item])
            elif item == const.START:
                my_dict[item] = datetime.strptime(my_dict[item], '%Y-%m-%d%H:%M:%S').replace(tzinfo=UTC)
            elif item == const.END:
                my_dict[item] = datetime.strptime(my_dict[item], '%Y-%m-%d%H:%M:%S').replace(tzinfo=UTC)
            elif item == const.WHITELIST_START:
                my_dict[item] = datetime.strptime(my_dict[item], '%Y-%m-%d%H:%M:%S').replace(tzinfo=UTC)
            elif item == const.WHITELIST_END:
                my_dict[item] = datetime.strptime(my_dict[item], '%Y-%m-%d%H:%M:%S').replace(tzinfo=UTC)
            elif item == const.WHITELIST:
                my_dict[item] = self._str_to_bool(my_dict[item])
            else:
                my_dict[item] = unicode(my_dict[item])

        return my_dict

    def _str_to_bool(self, input):
        if input.lower() == "true":
            return True
        elif input.lower() == "false":
            return False
        else:
            raise KeyError
