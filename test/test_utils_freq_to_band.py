import pytest
from pyhamtools.frequency import freq_to_band
from pyhamtools.consts import LookupConventions as const

class Test_utils_freq_to_band():

    def test_hf_frequencies(self):
        assert freq_to_band(137) == {"band" : 2190, "mode":const.CW}

        assert freq_to_band(1805) == {"band" : 160, "mode":const.CW}
        assert freq_to_band(1838) == {"band" : 160, "mode":const.DIGITAL}
        assert freq_to_band(1870) == {"band" : 160, "mode":const.LSB}

        assert freq_to_band(3500) == {"band" : 80, "mode":const.CW}
        assert freq_to_band(3580) == {"band" : 80, "mode":const.DIGITAL}
        assert freq_to_band(3799) == {"band" : 80, "mode":const.LSB}

        assert freq_to_band(5200) == {"band" : 60, "mode":None}

        assert freq_to_band(7000) == {"band" : 40, "mode":const.CW}
        assert freq_to_band(7044) == {"band" : 40, "mode":const.DIGITAL}
        assert freq_to_band(7139) == {"band" : 40, "mode":const.LSB}

        assert freq_to_band(10100) == {"band" : 30, "mode":const.CW}
        assert freq_to_band(10141) == {"band" : 30, "mode":const.DIGITAL}

        assert freq_to_band(14000) == {"band" : 20, "mode":const.CW}
        assert freq_to_band(14070) == {"band" : 20, "mode":const.DIGITAL}
        assert freq_to_band(14349) == {"band" : 20, "mode":const.USB}

        assert freq_to_band(18068) == {"band" : 17, "mode":const.CW}
        assert freq_to_band(18096) == {"band" : 17, "mode":const.DIGITAL}
        assert freq_to_band(18250) == {"band" : 17, "mode":const.USB}

        assert freq_to_band(21000) == {"band" : 15, "mode":const.CW}
        assert freq_to_band(21070) == {"band" : 15, "mode":const.DIGITAL}
        assert freq_to_band(21449) == {"band" : 15, "mode":const.USB}

        assert freq_to_band(24890) == {"band" : 12, "mode":const.CW}
        assert freq_to_band(24916) == {"band" : 12, "mode":const.DIGITAL}
        assert freq_to_band(24965) == {"band" : 12, "mode":const.USB}

        assert freq_to_band(28000) == {"band" : 10, "mode":const.CW}
        assert freq_to_band(28070) == {"band" : 10, "mode":const.DIGITAL}
        assert freq_to_band(28500) == {"band" : 10, "mode":const.USB}

        assert freq_to_band(50000) == {"band" : 6, "mode":const.CW}
        assert freq_to_band(50100) == {"band" : 6, "mode":const.USB}
        assert freq_to_band(50500) == {"band" : 6, "mode":const.DIGITAL}

    def test_vhf_frequencies(self):
        assert freq_to_band(70001) == {"band" : 4, "mode":None}

        assert freq_to_band(144000) == {"band" : 2, "mode":const.CW}
        assert freq_to_band(144150) == {"band" : 2, "mode":const.USB}
        assert freq_to_band(144400) == {"band" : 2, "mode":None}

        assert freq_to_band(220000) == {"band" : 1.25, "mode":None}

    def test_uhf_frequencies(self):
        assert freq_to_band(420000) == {"band" : 0.7, "mode":None}

        assert freq_to_band(902000) == {"band" : 0.33, "mode":None}

        assert freq_to_band(1200000) == {"band" : 0.23, "mode":None}

    def test_shf_frequencies(self):
        assert freq_to_band(2390000) == {"band" : 0.13, "mode":None}

        assert freq_to_band(3300000) == {"band" : 0.09, "mode":None}

        assert freq_to_band(5650000) == {"band" : 0.053, "mode":None}

        assert freq_to_band(10000000) == {"band" : 0.03, "mode":None}

        assert freq_to_band(24000000) == {"band" : 0.0125, "mode":None}

        assert freq_to_band(47000000) == {"band" : 0.0063, "mode":None}

        with pytest.raises(KeyError):
            freq_to_band(16304)

    def test_ft_frequencies(self):
        assert freq_to_band(1840) == {"band": 160, "mode": const.DIGITAL} #FT8
        assert freq_to_band(3573) == {"band": 80, "mode": const.DIGITAL} #FT8
        assert freq_to_band(7074) == {"band": 40, "mode": const.DIGITAL} #FT8
        assert freq_to_band(10136) == {"band": 30, "mode": const.DIGITAL} #FT8
        assert freq_to_band(14074) == {"band": 20, "mode": const.DIGITAL} #FT8
        assert freq_to_band(18100) == {"band": 17, "mode": const.DIGITAL} #FT8
        assert freq_to_band(21074) == {"band": 15, "mode": const.DIGITAL} #FT8
        assert freq_to_band(24915) == {"band": 12, "mode": const.DIGITAL} #FT8
        assert freq_to_band(28074) == {"band": 10, "mode": const.DIGITAL} #FT8
        assert freq_to_band(50313) == {"band": 6, "mode": const.DIGITAL} #FT8
        assert freq_to_band(144174.5) == {"band": 2, "mode": const.DIGITAL} #FT8