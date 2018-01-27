import pytest
from datetime import datetime
import pytz
import os

from pyhamtools.lookuplib import LookupLib
from pyhamtools.exceptions import APIKeyMissingError

UTC = pytz.UTC


#Fixtures
#===========================================================



response_Entity_230 = {
          'country': u'FEDERAL REPUBLIC OF GERMANY',
          'continent': u'EU',
          'latitude': 51.0,
          'longitude': 10.0,
          'cqz': 14,
          'prefix' : u'DL',
          'deleted' : False,
}

response_Exception_KC6MM_1990 = {
           'adif': 22,
           'country': u'PALAU',
           'continent': u'OC',
           'latitude': 9.50,
           'longitude': 138.20,
           'cqz': 27,
        }

response_Exception_KC6MM_1992 = {
           'adif': 22,
           'country': u'PALAU',
           'continent': u'OC',
           'latitude': 9.50,
           'longitude': 138.20,
           'cqz': 27,
        }

response_Exception_VK9XX_with_end_date = {
           'adif': 35,
           'country': u'CHRISTMAS ISLAND',
           'continent': u'OC',
           'latitude': -10.50,
           'longitude': 105.70,
           'cqz': 29,
        }

response_Exception_VK9XO_with_start_date = {
           'adif': 35,
           'country': u'CHRISTMAS ISLAND',
           'continent': u'OC',
           'latitude': -10.50,
           'longitude': 105.70,
           'cqz': 29,
        }

response_Exception_AX9NYG = {
           'adif': 38,
           'country': u'COCOS (KEELING) ISLAND',
           'continent': u'OC',
           'latitude': -12.20,
           'longitude': 96.80,
           'cqz': 29,
        }

response_Prefix_DH = {
    'country': u'FEDERAL REPUBLIC OF GERMANY',
    'adif' : 230,
    'continent': u'EU',
    'latitude': 51.0,
    'longitude': 10.0,
    'cqz': 14,
}

response_Prefix_VK9_until_1975 = {
    'country': u'PAPUA TERR',
    'adif' : 198,
    'continent': u'OC',
    'latitude': -9.40,
    'longitude': 147.10,
    'cqz': 28,
}

response_Prefix_VK9_starting_1976 = {
    'country': u'NORFOLK ISLAND',
    'adif' : 189,
    'continent': u'OC',
    'latitude': -29.00,
    'longitude': 168.00,
    'cqz': 32,
}

response_Prefix_ZD5_1964_to_1971 = {
    'country': u'SWAZILAND',
    'adif' : 468,
    'continent': u'AF',
    'latitude': -26.30,
    'longitude': 31.10,
    'cqz': 38,
}





@pytest.fixture(scope="function")
def fix_cty_xml_file(request):
    dir = os.path.dirname(__file__)
    cty_file_rel = "./fixtures/cty.xml"
    cty_file_abs = os.path.join(dir, cty_file_rel)
    return cty_file_abs


#TESTS
#===========================================================

class TestClublogXML_Constructor:

    def test_with_invalid_api_key(self):
        with pytest.raises(APIKeyMissingError):
            lib = LookupLib(lookuptype="clublogxml", apikey="foo")
            lib.lookup_entity(230)

    def test_with_no_api_key(self):
        with pytest.raises(APIKeyMissingError):
            lib = LookupLib(lookuptype="clublogxml")
            lib.lookup_entity(230)

    def test_with_file(self, fix_cty_xml_file):
        lib = LookupLib(lookuptype="clublogxml", filename=fix_cty_xml_file)
        assert lib.lookup_entity(230) == response_Entity_230

class TestclublogXML_Getters:

    #lookup_entity(callsign)
    #===============================

    def test_lookup_entity(self, fixClublogXML):
        assert fixClublogXML.lookup_entity(230) == response_Entity_230
        assert fixClublogXML.lookup_entity("230") == response_Entity_230

        with pytest.raises(ValueError):
            fixClublogXML.lookup_entity("foo")

        with pytest.raises(KeyError):
            fixClublogXML.lookup_entity(1000)

        with pytest.raises(KeyError):
            fixClublogXML.lookup_entity(999)


    #lookup_callsign(callsign, [date])
    #===============================

    def test_lookup_callsign_same_callsign_different_exceptions(self, fixClublogXML):
        timestamp = datetime(year=1990, month=10, day=12, tzinfo=UTC)
        assert fixClublogXML.lookup_callsign("kc6mm", timestamp) == response_Exception_KC6MM_1990

        timestamp = datetime(year=1992, month=3, day=8, tzinfo=UTC)
        assert fixClublogXML.lookup_callsign("kc6mm", timestamp) == response_Exception_KC6MM_1992

    def test_lookup_callsign_exception_only_with_start_date(self, fixClublogXML):
        #timestamp > startdate
        timestamp = datetime(year=1962, month=7, day=7, tzinfo=UTC)
        assert fixClublogXML.lookup_callsign("vk9xo", timestamp) == response_Exception_VK9XO_with_start_date
        assert fixClublogXML.lookup_callsign("vk9xo") == response_Exception_VK9XO_with_start_date

        #timestamp < startdate
        timestamp = datetime(year=1962, month=7, day=5, tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.lookup_callsign("vk9xo", timestamp)

    def test_lookup_callsign_exception_only_with_end_date(self, fixClublogXML):

        #timestamp < enddate
        timestamp = datetime(year=1975, month=9, day=14, tzinfo=UTC)
        assert fixClublogXML.lookup_callsign("vk9xx", timestamp) == response_Exception_VK9XX_with_end_date

        # timestamp > enddate
        with pytest.raises(KeyError):
            fixClublogXML.lookup_callsign("vk9xx")

        timestamp = datetime(year=1975, month=9, day=16, tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.lookup_callsign("vk9xx", timestamp)

    def test_lookup_callsign_exception_no_start_nor_end_date(self, fixClublogXML):

        timestamp = datetime(year=1975, month=9, day=14, tzinfo=UTC)
        assert fixClublogXML.lookup_callsign("ax9nyg", timestamp) == response_Exception_AX9NYG
        assert fixClublogXML.lookup_callsign("ax9nyg" ) == response_Exception_AX9NYG



    #lookup_prefix(prefix, [date])
    #=========================

    def test_lookup_prefix(self, fixClublogXML):
        assert fixClublogXML.lookup_prefix("DH") == response_Prefix_DH

        with pytest.raises(KeyError):
            fixClublogXML.lookup_prefix("QRM")

        with pytest.raises(KeyError):
            fixClublogXML.lookup_prefix("")


    def test_lookup_prefix_with_changing_entities(self, fixClublogXML):
        #return old entity (PAPUA TERR)
        timestamp = datetime(year=1975, month=9, day=14).replace(tzinfo=UTC)
        assert fixClublogXML.lookup_prefix("VK9", timestamp) == response_Prefix_VK9_until_1975

        #return empty dict - Prefix was not assigned at that time
        timestamp = datetime(year=1975, month=9, day=16).replace(tzinfo=UTC)

        with pytest.raises(KeyError):
            fixClublogXML.lookup_prefix("VK9", timestamp)

        #return new entity (Norfolk Island)
        timestamp = datetime.utcnow().replace(tzinfo=UTC)
        assert fixClublogXML.lookup_prefix("VK9", timestamp ) == response_Prefix_VK9_starting_1976

    def test_lookup_prefix_with_entities_having_start_and_stop(self, fixClublogXML):

        timestamp_before = datetime(year=1964, month=11, day=1).replace(tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.lookup_prefix("ZD5", timestamp_before)

        timestamp_valid = datetime(year=1964, month=12, day=2).replace(tzinfo=UTC)
        assert fixClublogXML.lookup_prefix("ZD5", timestamp_valid) == response_Prefix_ZD5_1964_to_1971

        timestamp_after = datetime(year=1971, month=8, day=1).replace(tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.lookup_prefix("ZD5", timestamp_after)



    #is_invalid_operation(callsign, [date])
    #====================================

    def test_is_invalid_operations(self, fixClublogXML):

        #No dataset --> default Operation is True
        with pytest.raises(KeyError):
            fixClublogXML.is_invalid_operation("dh1tw")

        #Invalid Operation with start and end date
        timestamp_before = datetime(year=1993, month=12, day=30).replace(tzinfo=UTC)
        timestamp = datetime(year=1994, month=12, day=30).replace(tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.is_invalid_operation("vk0mc")

        assert fixClublogXML.is_invalid_operation("vk0mc", timestamp)

        with pytest.raises(KeyError):
            fixClublogXML.is_invalid_operation("vk0mc", timestamp_before)

        #Invalid Operation with start date
        assert fixClublogXML.is_invalid_operation("5W1CFN")
        timestamp_before = datetime(year=2012, month=1, day=31).replace(tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.is_invalid_operation("5W1CFN", timestamp_before)

        #Invalid Operation with end date
        timestamp_before = datetime(year=2004, month=4, day=2).replace(tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.is_invalid_operation("T33C")

        assert fixClublogXML.is_invalid_operation("T33C", timestamp_before)



    #lookup_zone_exception(callsign, [date])
    #====================================

    def test_lookup_zone_exception(self, fixClublogXML):

        #No dataset --> default answer: None
        with pytest.raises(KeyError):
            fixClublogXML.lookup_zone_exception("dh1tw")

        #zone exception with no date
        assert fixClublogXML.lookup_zone_exception("dp0gvn") == 38

        #zone exception with start and end date
        timestamp = datetime(year=1992, month=10, day=2).replace(tzinfo=UTC)
        timestamp_before = datetime(year=1992, month=9, day=30).replace(tzinfo=UTC)
        timestamp_after = datetime(year=1993, month=3, day=1).replace(tzinfo=UTC)
        assert fixClublogXML.lookup_zone_exception("dl1kvc/p", timestamp) == 38

        with pytest.raises(KeyError):
            fixClublogXML.lookup_zone_exception("dl1kvc/p", timestamp_before)

        with pytest.raises(KeyError):
            fixClublogXML.lookup_zone_exception("dl1kvc/p", timestamp_after)

        #zone exception with start date
        timestamp_before = datetime(year=2013, month=12, day=26).replace(tzinfo=UTC)
        with pytest.raises(KeyError):
            fixClublogXML.lookup_zone_exception("dh1hb/p", timestamp_before)
