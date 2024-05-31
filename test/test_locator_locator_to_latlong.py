import pytest
import maidenhead
from pyhamtools.locator import locator_to_latlong
from pyhamtools.consts import LookupConventions as const


class Test_locator_to_latlong():

    def test_locator_to_latlong_min_max_cases(self):
        latitude, longitude = locator_to_latlong("AA00AA")
        assert abs(latitude + 89.97916) < 0.00001
        assert abs(longitude +179.95833) < 0.0001

        latitude, longitude = locator_to_latlong("RR99XX")
        assert abs(latitude - 89.97916) < 0.00001
        assert abs(longitude - 179.9583) < 0.0001

    def test_locator_to_latlong_4chars_precision(self):

        latitude, longitude = locator_to_latlong("JN48")
        assert abs(latitude - 48.5) < 0.1
        assert abs(longitude - 9.0) < 0.1

        latitude, longitude = locator_to_latlong("JN48", center=False)
        assert abs(latitude - 48) < 0.1
        assert abs(longitude - 8) < 0.1

    def test_locator_to_latlong_6chars_precision(self):
        latitude, longitude = locator_to_latlong("JN48QM")
        assert abs(latitude - 48.52083) < 0.00001
        assert abs(longitude - 9.37500) < 0.00001

    def test_locator_to_latlong_8chars(self):

        latitude, longitude = locator_to_latlong("JN48QM84")
        assert abs(latitude - 48.51875) < 0.00001
        assert abs(longitude - 9.40416) < 0.00001

        latitude, longitude = locator_to_latlong("EM69SF53")
        assert abs(latitude - 39.222916) < 0.00001
        assert abs(longitude + 86.45416) < 0.00001

    def test_locator_to_latlong_consistency_checks_6chars_lower_left_corner(self):

        latitude_4, longitude_4 = locator_to_latlong("JN48", center=False)
        latitude_6, longitude_6 = locator_to_latlong("JN48AA", center=False)

        assert latitude_4 == latitude_6
        assert longitude_4 == longitude_6

    def test_locator_to_latlong_consistency_checks_8chars_lower_left_corner(self):

        latitude_6, longitude_6 = locator_to_latlong("JN48AA", center=False)
        latitude_8, longitude_8 = locator_to_latlong("JN48AA00", center=False)

        assert latitude_6 == latitude_8
        assert longitude_6 == longitude_8

    def test_locator_to_latlong_consistency_checks_against_maidenhead(self):

        locs = ["JN48", "EM69", "JN48QM", "EM69SF", "AA00AA", "RR99XX", "JN48QM84", "EM69SF53"]

        # lower left (south/east) corner
        for loc in locs:
            lat, lon = locator_to_latlong(loc, center=False)
            lat_m, lon_m = maidenhead.to_location(loc)
            assert abs(lat - lat_m) < 0.00001
            assert abs(lon - lon_m) < 0.00001

        # center of square
        for loc in locs:
            lat, lon = locator_to_latlong(loc) # default: center=True
            lat_m, lon_m = maidenhead.to_location(loc, center=True)
            assert abs(lat - lat_m) < 0.1
            assert abs(lon - lon_m) < 0.1

    def test_locator_to_latlong_upper_lower_chars(self):

        latitude, longitude = locator_to_latlong("Jn48qM")
        assert abs(latitude - 48.52083) < 0.00001
        assert abs(longitude - 9.3750000) < 0.0001

    def test_locator_to_latlong_wrong_amount_of_characters(self):

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("J")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("JN")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("JN4")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("JN8Q")
        
        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("JN8QM1")

    def test_locator_to_latlong_invalid_characters(self):

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("21XM99")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("48")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("JNJN")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("JN4848")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("JN48QMaa")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("****")

    def test_locator_to_latlong_out_of_boundry(self):

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("RR99XY")
