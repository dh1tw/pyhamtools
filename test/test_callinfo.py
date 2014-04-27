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
    'longitude': -10.0,
    'cqz': 14,
}

response_prefix_DH_countryfile = {
    'country': 'Fed. Rep. of Germany',
    'adif': 230,
    'continent': 'EU',
    'latitude': 51.0,
    'longitude': -10.0,
    'cqz': 14,
    'ituz': 28
}

response_prefix_C6A_clublog = {
    'country': 'BAHAMAS',
    'longitude': 76.0,
    'cqz': 8,
    'adif': 60,
    'latitude': 24.25,
    'continent': 'NA'
}

response_prefix_C6A_countryfile = {
    'country': 'Bahamas',
    'longitude': 76.0,
    'cqz': 8,
    'adif': 60,
    'latitude': 24.25,
    'continent': 'NA',
    'ituz': 11
}



response_Exception_VK9XO_with_start_date = {
           'adif': 35,
           'country': 'CHRISTMAS ISLAND',
           'continent': 'OC',
           'latitude': -10.50,
           'longitude': -105.70,
           'cqz': 29
        }

response_zone_exception_dp0gvn = {
    'country': 'ANTARCTICA',
    'adif': 13,
    'cqz': 38,
    'latitude': -65.0,
    'longitude': 64.0,
    'continent': 'AN'
}

response_lat_long_dh1tw = {
    const.LATITUDE: 51.0,
    const.LONGITUDE: -10.0
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

    def test_get_homecall(self, fix_callinfo):
        assert fix_callinfo.get_homecall("HB9/DH1TW") == "DH1TW"
        assert fix_callinfo.get_homecall("SM3/DH1TW/P") == "DH1TW"
        assert fix_callinfo.get_homecall("QRM") is None

    def test_dismantle_callsign(self, fix_callinfo):
        if fix_callinfo._lookuplib._lookuptype == "clublogxml" or fix_callinfo._lookuplib._lookuptype == "countryfile":
            with pytest.raises(KeyError):
                fix_callinfo._dismantle_callsign("DH1TW/MM")

            with pytest.raises(KeyError):
                fix_callinfo._dismantle_callsign("DH1TW/AM")

        if fix_callinfo._lookuplib._lookuptype == "clublogxml":
            assert fix_callinfo._dismantle_callsign("DH1TW/QRP") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/QRPP") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/BCN") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/LH") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("HC2AO/DL") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/P") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/5") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/M") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/B") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DH1TW/B") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("DL/HC2AO") == response_prefix_DH_clublog
            assert fix_callinfo._dismantle_callsign("9H5A/C6A") == response_prefix_C6A_clublog
        #    assert fix_callinfo._dismantle_callsign("C6A/9H5A") == response_Prefix_C6A

        if fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo._dismantle_callsign("DH1TW/QRP") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/QRPP") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/BCN") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/LH") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("HC2AO/DL") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/P") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/5") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/M") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/B") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DH1TW/B") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("DL/HC2AO") == response_prefix_DH_countryfile
            assert fix_callinfo._dismantle_callsign("9H5A/C6A") == response_prefix_C6A_countryfile
        #    assert fix_callinfo._dismantle_callsign("C6A/9H5A") == response_Prefix_C6A


    def test_lookup_callsign(selfself, fix_callinfo):

        if fix_callinfo._lookuplib._lookuptype == "clublogxml" or fix_callinfo._lookuplib._lookuptype == "clublogapi":
            with pytest.raises(KeyError):
                fix_callinfo._lookup_callsign("5W1CFN")
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

        elif fix_callinfo._lookuplib._lookuptype == "countryfile":
            assert fix_callinfo.get_all("DH1TW") == response_prefix_DH_countryfile

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