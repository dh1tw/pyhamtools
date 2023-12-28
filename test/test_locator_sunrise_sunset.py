from datetime import datetime, timedelta, timezone

import pytest

from pyhamtools.locator import calculate_sunrise_sunset

class Test_calculate_sunrise_sunset_normal_case():

    def test_calculate_sunrise_sunset(self):

        time_margin = timedelta(minutes=1)
        locator = "JN48QM"

        test_time =  datetime(year=2014, month=1, day=1, tzinfo=timezone.utc)
        result_JN48QM_1_1_2014_evening_dawn = datetime(2014, 1, 1, 15, 38, tzinfo=timezone.utc)
        result_JN48QM_1_1_2014_morning_dawn = datetime(2014, 1, 1, 6, 36,  tzinfo=timezone.utc)
        result_JN48QM_1_1_2014_sunrise = datetime(2014, 1, 1, 7, 14, tzinfo=timezone.utc)
        result_JN48QM_1_1_2014_sunset = datetime(2014, 1, 1, 16, 15, 23, 31016, tzinfo=timezone.utc)

        assert calculate_sunrise_sunset(locator, test_time)['morning_dawn'] - result_JN48QM_1_1_2014_morning_dawn < time_margin
        assert calculate_sunrise_sunset(locator, test_time)['evening_dawn'] - result_JN48QM_1_1_2014_evening_dawn < time_margin
        assert calculate_sunrise_sunset(locator, test_time)['sunset'] - result_JN48QM_1_1_2014_sunset < time_margin
        assert calculate_sunrise_sunset(locator, test_time)['sunrise'] - result_JN48QM_1_1_2014_sunrise < time_margin


    def test_calculate_sunrise_sunset_with_sun_never_rising(self):

        time_margin = timedelta(minutes=1)
        locator = "IQ50PW"
        # The sun never rises in winter time close to the north pole (e.g. at Jan Mayen)
        # Therefore we expect no sunrise or sunset. 

        test_time =  datetime(year=2021, month=12, day=15, tzinfo=timezone.utc)

        assert calculate_sunrise_sunset(locator, test_time)['morning_dawn'] == None
        assert calculate_sunrise_sunset(locator, test_time)['evening_dawn'] == None
        assert calculate_sunrise_sunset(locator, test_time)['sunset'] == None
        assert calculate_sunrise_sunset(locator, test_time)['sunrise'] == None


    def test_calculate_sunrise_sunset_with_sun_never_setting(self):

        time_margin = timedelta(minutes=1)
        locator = "AA00AA"
        # The sun never sets at the south pole during arctic summer 
        # Therefore we expect no sunrise or sunset. 

        test_time =  datetime(year=2014, month=1, day=1, tzinfo=timezone.utc)

        assert calculate_sunrise_sunset(locator, test_time)['morning_dawn'] == None
        assert calculate_sunrise_sunset(locator, test_time)['evening_dawn'] == None
        assert calculate_sunrise_sunset(locator, test_time)['sunset'] == None
        assert calculate_sunrise_sunset(locator, test_time)['sunrise'] == None

    def test_calculate_distance_invalid_inputs(self):

        with pytest.raises(ValueError):
            calculate_sunrise_sunset("", "")

        with pytest.raises(ValueError):
            calculate_sunrise_sunset("JN48QM", "")

        with pytest.raises(ValueError):
            calculate_sunrise_sunset("JN48", 55)

        with pytest.raises(AttributeError):
            calculate_sunrise_sunset(33, datetime.now())
