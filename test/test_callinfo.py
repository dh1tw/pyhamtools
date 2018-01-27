from datetime import datetime

import pytest
import pytz

from pyhamtools.consts import LookupConventions as const

UTC = pytz.UTC


response_prefix_DH_clublog = {
    'country': 'FEDERAL REPUBLIC OF GERMANY',
    'adif': 230,
    'continent': 'EU',
    'latitude': 51.0,
    'longitude': 10.0,
    'cqz': 14,
}

response_prefix_DH_countryfile = {
    'country': 'Fed. Rep. of Germany',
    'adif': 230,
    'continent': 'EU',
    'latitude': 51.0,
    'longitude': 10.0,
    'cqz': 14,
    'ituz': 28
}

response_prefix_C6A_clublog = {
    'country': 'BAHAMAS',
    'longitude': -76.0,
    'cqz': 8,
    'adif': 60,
    'latitude': 24.25,
    'continent': 'NA'
}

response_prefix_C6A_countryfile = {
    'country': 'Bahamas',
    'longitude': -76.0,
    'cqz': 8,
    'adif': 60,
    'latitude': 24.25,
    'continent': 'NA',
    'ituz': 11
}

response_prefix_VK9NDX_countryfile = {
    u'adif': 189,
    u'continent': u'OC',
    u'country': u'Norfolk Island',
    u'cqz': 32,
    u'ituz': 60,
    u'latitude': -29.03,
    u'longitude': 167.93
}

response_prefix_VK9DNX_clublog = {
    u'adif': 189,
    u'continent': u'OC',
    u'country': u'NORFOLK ISLAND',
    u'cqz': 32,
    u'latitude': -29.0,
    u'longitude': 168.0
}

response_prefix_VK9DWX_clublog = {
    u'adif': 303,
    u'continent': u'OC',
    u'country': u'WILLIS ISLAND',
    u'cqz': 30,
    u'latitude': -16.2,
    u'longitude': 150.0
}

response_prefix_VK9DLX_clublog = {
    u'adif': 147,
    u'continent': u'OC',
    u'country': u'LORD HOWE ISLAND',
    u'cqz': 30,
    u'latitude': -31.6,
    u'longitude': 159.1
}

response_prefix_VK9DLX_countryfile = {
     u'adif': 147,
     u'continent': u'OC',
     u'country': u'Lord Howe Island',
     u'cqz': 30,
     u'ituz': 60,
     u'latitude': -31.55,
     u'longitude': 159.08
}

response_prefix_VK9GMW_clublog = {
    u'adif': 171,
    u'continent': u'OC',
    u'country': u'MELLISH REEF',
    u'cqz': 30,
    u'latitude': -17.6,
    u'longitude': 155.8
}

response_callsign_exceptions_7N1PRD_0_clublog = {
    u'adif': 339,
    u'continent': u'AS',
    u'country': u'JAPAN',
    u'cqz': 25,
    u'latitude': 35.7,
    u'longitude': 139.8
}

response_callsign_exceptions_SV8GXQ_P_QRP_clublog = {
    u'adif': 236,
    u'continent': u'EU',
    u'country': u'GREECE',
    u'cqz': 20,
    u'latitude': 38.0,
    u'longitude': 23.7
}

response_Exception_VP8STI_with_start_and_stop_date = {
           'adif': 240,
           'country': u'SOUTH SANDWICH ISLANDS',
           'continent': u'SA',
           'latitude': -59.45,
           'longitude': -27.4,
           'cqz': 13,
        }


response_Exception_VK9XO_with_start_date = {
           'adif': 35,
           'country': 'CHRISTMAS ISLAND',
           'continent': 'OC',
           'latitude': -10.50,
           'longitude': 105.70,
           'cqz': 29
        }

response_zone_exception_dp0gvn = {
    'country': 'ANTARCTICA',
    'adif': 13,
    'cqz': 38,
    'latitude': -65.0,
    'longitude': -64.0,
    'continent': 'AN'
}

response_lat_long_dh1tw = {
    const.LATITUDE: 51.0,
    const.LONGITUDE: 10.0
}

response_maritime_mobile = {
    'adif': 999,
    'continent': '',
    'country': 'MARITIME MOBILE',
    'cqz': 0,
    'latitude': 0.0,
    'longitude': 0.0
}

response_aircraft_mobile = {
    'adif': 998,
    'continent': '',
    'country': 'AIRCAFT MOBILE',
    'cqz': 0,
    'latitude': 0.0,
    'longitude': 0.0
}

response_callsign_exceptions_7QAA_clublog = {
    u'adif': 440,
    u'continent': u'AF',
    u'country': u'MALAWI',
    u'cqz': 37,
    u'latitude': -14.9,
    u'longitude': 34.4
}




class Test_callinfo_methods:

    def test_callinfo_iterate_prefix(self, fix_callinfo):
        if fix_callinfo._lookuplib._lookuptype == "clublogxml":
            assert fix_callinfo._iterate_prefix("DH1TW") == response_prefix_DH_clublog

            with pytest.raises(KeyError):
                fix_callinfo._iterate_prefix("QRM")

        if fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo._iterate_prefix("DH1TW") == response_prefix_DH_countryfile

            with pytest.raises(KeyError):
                fix_callinfo._iterate_prefix("QRM")

    def test_is_maritime_mobile(self, fix_callinfo):
        assert fix_callinfo.check_if_mm("DH1TW/MM")
        assert not fix_callinfo.check_if_mm("DH1TW")

    def test_is_aircraft_mobile(self, fix_callinfo):
        assert fix_callinfo.check_if_am("DH1TW/AM")
        assert not fix_callinfo.check_if_am("DH1TW")

    def test_if_beacon(self, fix_callinfo):
        assert fix_callinfo.check_if_beacon("DH1TW/B")
        assert fix_callinfo.check_if_beacon("DH1TW/BCN")
        assert not fix_callinfo.check_if_beacon("DH1TW")

    def test_get_homecall(self, fix_callinfo):
        assert fix_callinfo.get_homecall("HB9/DH1TW") == "DH1TW"
        assert fix_callinfo.get_homecall("SM3/DH1TW/P") == "DH1TW"
        with pytest.raises(ValueError):
            fix_callinfo.get_homecall("QRM")

    def test_dismantle_callsign(self, fix_callinfo):

        if fix_callinfo._lookuplib._lookuptype == "clublogxml":
            assert fix_callinfo._dismantle_callsign("DH1TW/BCN")[const.BEACON]
            assert fix_callinfo._dismantle_callsign("DH1TW/QRP") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/QRPP") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/LH") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("HC2AO/DL") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/P") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/5") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/M") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/B")[const.BEACON]
            assert fix_callinfo._dismantle_callsign("DH1TW") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DL/HC2AO") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("9H5A/C6A") == response_prefix_C6A_clublog
            assert fix_callinfo._dismantle_callsign("C6A/9H5A") == response_prefix_C6A_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/UNI") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/BUX") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/NOT") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("VK9DLX/NOT") == response_prefix_VK9DLX_clublog
            assert fix_callinfo._dismantle_callsign("7QAA") == response_callsign_exceptions_7QAA_clublog
            assert fix_callinfo._dismantle_callsign("7N1PRD/0") == response_callsign_exceptions_7N1PRD_0_clublog
            assert fix_callinfo._dismantle_callsign("SV8GXQ/P/QRP") == response_callsign_exceptions_SV8GXQ_P_QRP_clublog

            with pytest.raises(KeyError):
                fix_callinfo._dismantle_callsign("OZ/JO85")

        if fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo._dismantle_callsign("DH1TW/QRP") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/QRPP") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/BCN")[const.BEACON]
            assert fix_callinfo._dismantle_callsign("DH1TW/LH") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("HC2AO/DL") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/P") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/5") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/M") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/B")[const.BEACON]
            assert fix_callinfo._dismantle_callsign("DH1TW") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DL/HC2AO") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("9H5A/C6A") == response_prefix_C6A_countryfile
            assert fix_callinfo._dismantle_callsign("C6A/9H5A") == response_prefix_C6A_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/NOT") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("VK9DLX/NOT") == response_prefix_VK9DLX_countryfile

            with pytest.raises(KeyError):
                fix_callinfo._dismantle_callsign("OZ/JO85")


    def test_dismantle_callsign_with_VK9_special_suffixes(self, fix_callinfo):

        if fix_callinfo._lookuplib._lookuptype == "clublog":
            assert fix_callinfo._dismantle_callsign("VK9DNX") == response_prefix_VK9DNX_clublog
            assert fix_callinfo._dismantle_callsign("VK9DLX") == response_prefix_VK9DLX_clublog
            assert fix_callinfo._dismantle_callsign("VK9GMX") == response_prefix_VK9GMW_clublog
            assert fix_callinfo._dismantle_callsign("VK9DWX") == response_prefix_VK9DWX_clublog


    def test_lookup_callsign(self, fix_callinfo):

        assert fix_callinfo._lookup_callsign("DH1TW/MM") == response_maritime_mobile
        assert fix_callinfo._lookup_callsign("DH1TW/AM") == response_aircraft_mobile

        if fix_callinfo._lookuplib._lookuptype == "clublogxml" or fix_callinfo._lookuplib._lookuptype == "clublogapi":
            with pytest.raises(KeyError):
                fix_callinfo._lookup_callsign("5W1CFN")

            assert fix_callinfo._lookup_callsign("DH1TW/BCN")[const.BEACON]
            assert fix_callinfo._lookup_callsign("VK9XO") == response_Exception_VK9XO_with_start_date
            assert fix_callinfo._lookup_callsign("DH1TW") == response_prefix_DH_clublog


        elif fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo._lookup_callsign("DH1TW") == response_prefix_DH_countryfile
            with pytest.raises(KeyError):
                fix_callinfo._lookup_callsign("QRM")

    def test_get_all(self, fix_callinfo):

        with pytest.raises(KeyError):
            fix_callinfo.get_all("QRM")

        if fix_callinfo._lookuplib._lookuptype == "clublogxml" or fix_callinfo._lookuplib._lookuptype == "clublogapi":
            assert fix_callinfo.get_all("DH1TW") == response_prefix_DH_clublog
            assert fix_callinfo.get_all("dp0gvn") == response_zone_exception_dp0gvn
            timestamp = datetime(year=2016, month=1, day=20, tzinfo=UTC)
            assert fix_callinfo.get_all("VP8STI", timestamp) == response_Exception_VP8STI_with_start_and_stop_date

        elif fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo.get_all("DH1TW") == response_prefix_DH_countryfile

        assert fix_callinfo.get_all("DH1TW/MM") == response_maritime_mobile

    def test_is_valid_callsign(self, fix_callinfo):
        assert fix_callinfo.is_valid_callsign("DH1TW")
        assert not fix_callinfo.is_valid_callsign("QRM")

    def test_get_lat_long(self, fix_callinfo):
        assert fix_callinfo.get_lat_long("DH1TW") == response_lat_long_dh1tw

        with pytest.raises(KeyError):
            fix_callinfo.get_lat_long("QRM")

    def test_get_cqz(self, fix_callinfo):
        assert fix_callinfo.get_cqz("DH1TW") == 14

        with pytest.raises(KeyError):
            fix_callinfo.get_cqz("QRM")

    def test_get_ituz(self, fix_callinfo):
        if fix_callinfo._lookuplib._lookuptype == "clublogxml" or fix_callinfo._lookuplib._lookuptype == "clublogapi":
            with pytest.raises(KeyError):
                fix_callinfo.get_ituz("DH1TW")

        elif fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo.get_ituz("DH1TW") == 28
            with pytest.raises(KeyError):
                fix_callinfo.get_ituz("QRM")

    def test_get_country(self, fix_callinfo):
        if fix_callinfo._lookuplib._lookuptype == "clublogxml" or fix_callinfo._lookuplib._lookuptype == "clublogapi":
            assert fix_callinfo.get_country_name("DH1TW") == 'FEDERAL REPUBLIC OF GERMANY'
            with pytest.raises(KeyError):
                fix_callinfo.get_country_name("QRM")

        elif fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo.get_country_name("DH1TW") == 'Fed. Rep. of Germany'
            with pytest.raises(KeyError):
                fix_callinfo.get_country_name("QRM")

    def test_get_adif_id(self, fix_callinfo):
        assert fix_callinfo.get_adif_id("DH1TW") == 230
        with pytest.raises(KeyError):
                fix_callinfo.get_adif_id("QRM")

    def test_get_continent(self, fix_callinfo):
        assert fix_callinfo.get_continent("DH1TW") == 'EU'
        with pytest.raises(KeyError):
                fix_callinfo.get_adif_id("QRM")
