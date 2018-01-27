import pytest
from pyhamtools.locator import latlong_to_locator
from pyhamtools.consts import LookupConventions as const

class Test_latlong_to_locator():

    def test_latlong_to_locator_edge_cases(self):
        assert latlong_to_locator(-89.97916, -179.95833) == "AA00AA"
        assert latlong_to_locator(89.97916, 179.9583) == "RR99XX"

    def test_latlong_to_locator_normal_case(self):

        assert latlong_to_locator(48.52083, 9.3750000) == "JN48QM"
        assert latlong_to_locator(48.5, 9.0) == "JN48MM" #center of the square

    def test_latlong_to_locator_invalid_characters(self):

        # throws ValueError in Python2 and TypeError in Python3
        with pytest.raises(Exception):
            latlong_to_locator("JN48QM", "test")

        # throws ValueError in Python2 and TypeError in Python3
        with pytest.raises(Exception):
            latlong_to_locator("", "")

    def test_latlong_to_locator_out_of_boundry(self):

        with pytest.raises(ValueError):
            latlong_to_locator(-90, -180)

        with pytest.raises(ValueError):
            latlong_to_locator(90, 180)

        with pytest.raises(ValueError):
            latlong_to_locator(10000, 120000)
