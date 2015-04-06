import pytest
from datetime import datetime


from apikey import QRZ_USERNAME, QRZ_PWD
from pyhamtools.lookuplib import LookupLib
from pyhamtools.exceptions import APIKeyMissingError
from pyhamtools.consts import LookupConventions as const

import pytz
UTC = pytz.UTC

#Fixtures
#===========================================================

response_XX1XX = {
#    'u_views': u'17495', 
    u'biodate': datetime(2015, 2, 4, 17, 50, 32, tzinfo=UTC),
    u'image': u'http://files.qrz.com/x/xx1xx/DSC_0094.png', 
    u'locator': u'KF05nx', 
    u'addr2': u'TEST CALLSIGN CITY', 
    u'addr1': u'DO NOT QSL', 
    u'aliases': [u'YY1YY'], 
    u'codes': u'TPS', 
    u'zipcode': u'010101', 
    u'lotw': True, 
    u'state': u'JC', 
    u'callsign': u'XX1XX', 
    u'fname': u'James W.', 
    u'latitude': -34.010735, 
    u'longitude': 21.164476,
    u'email': u'trucker2345@easymail.com', 
    u'qslmgr': u'NO QSL - TEST CALLSIGN', 
    u'bio': u'10415', 
    u'ccode': 120, 
    u'geoloc': u'user', 
    u'eqsl': True,
    u'mqsl': True, 
    u'adif': 134, 
    u'moddate': datetime(2015, 2, 4, 17, 53, 2, tzinfo=UTC),
    u'license_class': u'z', 
    u'land': u'Kingman Reef', 
    u'imageinfo': u'425:640:425545', 
    u'name': 'Smith', 
    u'born': 2002, 
    u'country': u'Iceland',
    u'user': u'XX1XX'
}

 
response_XX2XX = {
    u'bio': u'93', 
    u'land': u'NON-DXCC', 
    u'adif': 0, 
    u'zipcode': u'23232', 
    u'country': u'Anguilla', 
    u'user': u'XX2XX', 
    u'moddate': datetime(2015, 3, 20, 23, 20, 37, tzinfo=UTC),
    u'lotw': False, 
    u'ccode': 9, 
    u'geoloc': u'dxcc', 
    u'state': u'GA', 
    u'eqsl': False, 
    u'addr2': u'Las Vegas', 
#    'u_views': u'23', 
    u'fname': u'NO', 
    u'addr1': u'123 Main Stod\u00DFer', 
    u'callsign': u'XX2XX', 
    u'mqsl': False,
    u'biodate': datetime(2015, 2, 19, 22, 30, 2, tzinfo=UTC),
    u'image': u'http://files.qrz.com/x/xx2xx/oval_bumper_sticker4.png',
    u'imageinfo': u'285:500:44218'
} 

response_XX3XX = {
#    'u_views': u'4698', 
    u'biodate': datetime(2014, 8, 13, 15, 34, 57, tzinfo=UTC), 
    u'image': u'http://files.qrz.com/x/xx3xx/IMG_8813.JPG', 
    u'locator': u'FO51sj', 
    u'addr2': u'Shady Circle Roads', 
    u'addr1': u'1234 Main St.3', 
    u'aliases': [u'XX3XX/W7'], 
    u'zipcode': u'00033', 
    u'lotw': False, 
    u'state': u'JJ', 
    u'callsign': u'XX3XX', 
    u'fname': u'TEST\xc3\x9c\xc3\x9f\xc3\xb8x', 
    u'latitude': 51.396953, 
    u'email': u'fred@qrz.com', 
    u'qslmgr': u'Via BURO or AA7BQ', 
    u'bio': u'2420', 
    u'ccode': 130, 
    u'geoloc': u'user', 
    u'eqsl': False, 
    u'user': u'KF7WIS', 
    u'adif': 79, 
    u'moddate': datetime(2014, 6, 6, 23, 0, 45, tzinfo=UTC), 
    u'license_class': u'3', 
    u'land': u'Guadeloupe', 
    u'imageinfo': u'540:799:101014', 
    u'name': u'CALLSIGN3', 
    u'born': 2010, 
    u'country': u'Jamaica', 
    u'longitude': -68.41959,
    u'mqsl': False
}

response_XX4XX = {
#    'u_views': u'7980', 
    u'biodate': datetime(2014, 9, 17, 19, 46, 54, tzinfo=UTC), 
    u'image': u'http://files.qrz.com/x/xx4xx/IMG_0032.JPG', 
    u'locator': u'DM79mp', 
    u'addr2': u'Getamap and Findit', 
    u'addr1': u'Test Callsign for QRZ', 
    u'imageinfo': u'1200:1600:397936', 
    u'lotw': False, 
    u'state': u'ZZ', 
    u'callsign': u'XX4XX', 
    u'fname': u'Arthur', 
    u'latitude': 39.645, 
    u'iota': u'NA-075', 
    u'qslmgr': u'NO QSL - TEST CALLSIGN', 
    u'bio': u'785', 
    u'ccode': 34, 
    u'geoloc': u'user', 
    u'eqsl': False, 
    u'user': u'XX2XX', 
    u'adif': 64, 
    u'moddate': datetime(2014, 3, 28, 20, 29, 42, tzinfo=UTC), 
    u'name': u'Fay', 
    u'land': u'Bermuda', 
    u'zipcode': u'12345', 
    u'country': u'Bermuda', 
    u'longitude': -104.96,
    u'mqsl': False
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
        data = fix_qrz._lookup_qrz_callsign("xx1xx", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX1XX #check content 
        assert len(data) == len(response_XX1XX) #ensure all fields are included
        
        data = fix_qrz._lookup_qrz_callsign("XX1XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX1XX
        
        data = fix_qrz._lookup_qrz_callsign("XX2XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX2XX
        assert len(data) == len(response_XX2XX)
        
        data = fix_qrz._lookup_qrz_callsign("XX3XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX3XX
        assert len(data) == len(response_XX3XX)
        
        data = fix_qrz._lookup_qrz_callsign("XX4XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX4XX
        assert len(data) == len(response_XX4XX)
        
    def test_lookup_callsign_with_unicode_escaping(self, fix_qrz):
        data = fix_qrz._lookup_qrz_callsign("XX2XX", fix_qrz._apikey)
        data.pop('u_views', None)
        assert data == response_XX2XX
        
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
        