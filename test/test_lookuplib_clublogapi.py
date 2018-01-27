import pytest
from datetime import datetime

from pyhamtools.lookuplib import LookupLib

from pyhamtools.exceptions import APIKeyMissingError

#Fixtures
#===========================================================

response_Exception_DH1TW = {
          'adif': 230,
          'country': u'FEDERAL REPUBLIC OF GERMANY',
          'continent': u'EU',
          'latitude': 51.0,
          'longitude': -10.0,
          'cqz': 14
        }

response_Exception_VU9KV = {
          'adif': 324,
          'country': u'INDIA',
          'continent': u'AS',
          'latitude': 22.0,
          'longitude': -80.0,
          'cqz': 22
        }


response_Exception_VU9KV_with_Date = {
          'adif': 11,
          'country': u'ANDAMAN & NICOBAR ISLANDS',
          'continent': u'AS',
          'latitude': 11.70,
          'longitude': -92.80,
          'cqz': 26
        }


response_Exception_DH1TW_MM = {
        'adif': 999,
        'country': u'MARITIME MOBILE',
        'continent': u'',
        'latitude': 0.0,
        'longitude': 0.0,
        'cqz': 0
    }

response_Exception_DH1TW_AM = {
        'adif': 998,
        'country': u'AIRCRAFT MOBILE',
        'continent': u'',
        'longitude': 0.0,
        'latitude': 0.0,
        'cqz': 0
    }

#TESTS
#===========================================================

class TestClublogApi_Constructor:

    def test_with_invalid_api_key(self):
        with pytest.raises(APIKeyMissingError):
            lib = LookupLib(lookuptype="clublogapi", apikey="foo")
            lib.lookup_callsign("DH1TW")

    def test_with_no_api_key(self):
        with pytest.raises(APIKeyMissingError):
            lib = LookupLib(lookuptype="clublogapi")
            lib.lookup_callsign("DH1TW")

class TestclublogApi_Getters:

    #getEntity(adif)
    #===============================
    def test_lookup_callsign(self, fixClublogApi):
        assert fixClublogApi.lookup_entity(230) is None


    #lookup_callsign(callsign, [date])
    #===============================

    def test_lookup_callsign(self, fixClublogApi):
        assert fixClublogApi.lookup_callsign("DH1TW") == response_Exception_DH1TW
        assert fixClublogApi.lookup_callsign("VU9KV") == response_Exception_VU9KV
        d = datetime.utcnow().replace(year=1971, month=4, day=14)
        assert fixClublogApi.lookup_callsign("VU9KV", d) == response_Exception_VU9KV_with_Date
        assert fixClublogApi.lookup_callsign("DH1TW/MM") == response_Exception_DH1TW_MM
        assert fixClublogApi.lookup_callsign("DH1TW/AM") == response_Exception_DH1TW_AM

        with pytest.raises(KeyError):
            fixClublogApi.lookup_callsign("QRM")
        with pytest.raises(KeyError):
            fixClublogApi.lookup_callsign("")

    #lookup_prefix(prefix, [date])
    #===============================
    def test_lookup_callsign(self, fixClublogApi):
        with pytest.raises(KeyError):
            fixClublogApi.lookup_prefix("DH")


    #is_invalid_operation(callsign, [date])
    #===============================
    def test_is_invalid_operation(self, fixClublogApi):
        with pytest.raises(KeyError):
            fixClublogApi.is_invalid_operation("5W1CFN")


    #lookup_zone_exception(callsign, [date])
    #====================================
    def test_lookup_zone_exception(self, fixClublogApi):
        with pytest.raises(KeyError):
            fixClublogApi.lookup_zone_exception("dp0gvn")
