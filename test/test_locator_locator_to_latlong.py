import pytest
from pyhamtools.locator import locator_to_latlong
from pyhamtools.consts import LookupConventions as const

class Test_locator_to_latlong():

    def test_locator_to_latlong_edge_cases(self):
        latitude, longitude = locator_to_latlong("AA00AA")
        assert abs(latitude + 89.97916) < 0.00001
        assert abs(longitude +179.95833) < 0.0001

        latitude, longitude = locator_to_latlong("RR99XX")
        assert abs(latitude - 89.97916) < 0.00001
        assert abs(longitude - 179.9583) < 0.0001

    def test_locator_to_latlong_normal_case(self):

        latitude, longitude = locator_to_latlong("JN48QM")
        assert abs(latitude - 48.52083) < 0.00001
        assert abs(longitude - 9.3750000) < 0.0001

        latitude, longitude = locator_to_latlong("JN48")
        assert abs(latitude - 48.5) < 0.001
        assert abs(longitude - 9.000) < 0.001

    def test_locator_to_latlong_mixed_signs(self):

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

    def test_locator_to_latlong_invalid_characters(self):

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("21XM99")

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("****")

    def test_locator_to_latlong_out_of_boundry(self):

        with pytest.raises(ValueError):
            latitude, longitude = locator_to_latlong("RR99XY")
