import pytest
from pyhamtools.locator import calculate_distance, calculate_distance_longpath, calculate_heading, calculate_heading_longpath
from pyhamtools.consts import LookupConventions as const

class Test_calculate_distance():

    def test_calculate_distance_edge_cases(self):

        assert calculate_distance("JN48QM", "JN48QM") == 0
        assert calculate_distance("JN48", "JN48") == 0
        assert abs(calculate_distance("AA00AA", "rr00xx") - 19009) < 1

    def test_calculate_distance_normal_case(self):

        assert abs(calculate_distance("JN48QM", "FN44AB") - 5965) < 1
        assert abs(calculate_distance("FN44AB", "JN48QM") - 5965) < 1
        assert abs(calculate_distance("JN48QM", "QF67bf") - 16467) < 1

    def test_calculate_distance_invalid_inputs(self):
        with pytest.raises(AttributeError):
            calculate_distance(5, 12)

        with pytest.raises(ValueError):
            calculate_distance("XX0XX", "ZZ0Z")

    def test_calculate_distance_longpath_normal_case(self):

        assert abs(calculate_distance_longpath("JN48QM", "FN44AB") - 34042) < 1
        assert abs(calculate_distance_longpath("JN48QM", "QF67bf") - 23541) < 1

    def test_calculate_distance_longpath_edge_cases(self):

        assert abs(calculate_distance_longpath("JN48QM", "JN48QM") - 40008) < 1
        assert abs(calculate_distance_longpath("JN48QM", "AE15UU") - 20645) < 1 #ZL7 Chatham - almost antipods


class Test_calculate_heading():

    def test_calculate_heading_normal_cases(self):

        assert abs(calculate_heading("JN48QM", "FN44AB") - 298) < 1
        assert abs(calculate_heading("FN44AB", "JN48QM") - 54) < 1
        assert abs(calculate_heading("JN48QM", "QF67bf") - 74) < 1
        assert abs(calculate_heading("QF67BF", "JN48QM") - 310) < 1

    def test_calculate_heading_edge_cases(self):

        assert abs(calculate_heading("JN48QM", "JN48QM") - 0 ) < 1

    def test_calculate_heading_longpath(self):

        assert abs(calculate_heading_longpath("JN48QM", "FN44AB") - 118) < 1
        assert abs(calculate_heading_longpath("FN44AB", "JN48QM") - 234) < 1
        assert abs(calculate_heading_longpath("JN48QM", "QF67BF") - 254) < 1
        assert abs(calculate_heading_longpath("QF67BF", "JN48QM") - 130) < 1

    def test_calculate_heading_longpath_edge_cases(self):

        assert abs(calculate_heading_longpath("JN48QM", "JN48QM") - 180 ) < 1
