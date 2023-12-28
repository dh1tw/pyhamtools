import os

import pytest
from datetime import datetime, timezone

from pyhamtools.lookuplib import LookupLib
from pyhamtools.exceptions import APIKeyMissingError
from pyhamtools.consts import LookupConventions as const

try:
    QRZ_USERNAME = str(os.environ['QRZ_USERNAME'])
    QRZ_PWD = str(os.environ['QRZ_PWD'])
except Exception:
    pytestmark = pytest.mark.skip("Environment variables with QRZ.com credentials not set")

#Fixtures
#===========================================================

response_1A1AB = {
    u'biodate': datetime(2018, 9, 7, 21, 17, 7, tzinfo=timezone.utc),
    u'bio': u'0',
    u'license_class': u'C',
    u'moddate': datetime(2008, 11, 2, 15, 0, 38, tzinfo=timezone.utc),
    u'locator': u'JN61fw',
    u'callsign': u'1A1AB',
    u'addr2': u'00187  Rome',
    u'user': u'1A1AB',
    u'adif': 246,
    u'addr1': u'Via Condotti, 68',
    u'mqsl': True,
    u'ccode': 128,
    u'land': u'SMO Malta',
    u'codes': u'HVB',
    u'name': u'Morgan',
    u'geoloc': u'user',
    u'country': u'Italy',
    u'lotw': True,
    u'longitude': 12.456779,
    u'eqsl': True,
    u'fname': u'Jonas',
    u'latitude': 41.94417
    }

response_333 = {
    const.COUNTRY: u'Iraq',
    u'cc': u'IQ',
    const.LONGITUDE: 44.362793,
    const.CQZ: 21,
    const.ITUZ: 39,
    const.LATITUDE: 33.358062,
    u'timezone': 3.0,
    const.ADIF: 333,
    const.CONTINENT: u'AS',
    u'ccc': u'IRQ'
}

#TESTS
#===========================================================


class TestQrzConstructur:

    def test_get_session_key(self):
        lib = LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd=QRZ_PWD)
        assert len(lib._apikey) == 32

    def test_get_session_key_with_invalid_username(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username="hello", pwd=QRZ_PWD)

    def test_get_session_key_with_invalid_password(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd="hello")

    def test_get_session_key_with_empty_username_and_password(self):
        with pytest.raises(ValueError):
            lib = LookupLib(lookuptype="qrz", username="", pwd="")


class TestQrz_Callsign_Lookup:

    def test_lookup_callsign(self, fix_qrz):

        data = fix_qrz._lookup_qrz_callsign("1A1AB", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_1A1AB
        assert len(data) == len(response_1A1AB)

    def test_lookup_callsign_with_unicode_escaping(self, fix_qrz):
        data = fix_qrz._lookup_qrz_callsign("1A1AB", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_1A1AB

    def test_lookup_callsign_does_not_exist(self, fix_qrz):
        with pytest.raises(KeyError):
            fix_qrz._lookup_qrz_callsign("XX8XX", fix_qrz._apikey)

    def test_lookup_callsign_with_empty_input(self, fix_qrz):
        with pytest.raises(ValueError):
            fix_qrz._lookup_qrz_callsign("", fix_qrz._apikey)

    def test_lookup_callsign_with_invalid_input(self, fix_qrz):
        with pytest.raises(AttributeError):
            fix_qrz._lookup_qrz_callsign(3, fix_qrz._apikey)


class TestQrz_DXCC_Lookup:

    def test_lookup_dxcc_with_int(self, fix_qrz):
        data = fix_qrz._lookup_qrz_dxcc(333, fix_qrz._apikey)
        assert data == response_333 #check content
        assert len(data) == len(response_333) #ensure all fields are included

    def test_lookup_dxcc_with_string(self, fix_qrz):
        data = fix_qrz._lookup_qrz_dxcc("333", fix_qrz._apikey)
        assert data == response_333 #check content
        assert len(data) == len(response_333) #ensure all fields are included

    def test_lookup_dxcc_does_not_exist(self, fix_qrz):
        with pytest.raises(KeyError):
            fix_qrz._lookup_qrz_dxcc('854', fix_qrz._apikey)

    def test_lookup_dxcc_wrong_input(self, fix_qrz):
        with pytest.raises(ValueError):
            fix_qrz._lookup_qrz_dxcc('', fix_qrz._apikey)

    def test_lookup_dxcc(self, fix_qrz):
        data = fix_qrz.lookup_entity(333)
        assert data == response_333 #check content
