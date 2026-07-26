import pytest
from pyhamtools.frequency import freq_to_band
from pyhamtools.consts import LookupConventions as const

class Test_utils_freq_to_band():

    def test_hf_frequencies(self):
        assert freq_to_band(137) == {"band" : 2190, "adif": "2190m", "itu": "LF", "mode":const.CW}

        assert freq_to_band(472) == {"band" : 630, "adif": "630m", "itu": "MF", "mode":None}

        assert freq_to_band(502) == {"band" : 560, "adif": "560m", "itu": "MF", "mode":None}

        assert freq_to_band(1805) == {"band" : 160, "adif": "160m", "itu": "MF", "mode":const.CW}
        assert freq_to_band(1838) == {"band" : 160, "adif": "160m", "itu": "MF", "mode":const.DIGITAL}
        assert freq_to_band(1870) == {"band" : 160, "adif": "160m", "itu": "MF", "mode":const.LSB}

        assert freq_to_band(3500) == {"band" : 80, "adif": "80m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(3580) == {"band" : 80, "adif": "80m", "itu": "HF", "mode":const.DIGITAL}
        assert freq_to_band(3799) == {"band" : 80, "adif": "80m", "itu": "HF", "mode":const.LSB}

        assert freq_to_band(5200) == {"band" : 60, "adif": "60m", "itu": "HF", "mode":None}

        assert freq_to_band(7000) == {"band" : 40, "adif": "40m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(7044) == {"band" : 40, "adif": "40m", "itu": "HF", "mode":const.DIGITAL}
        assert freq_to_band(7139) == {"band" : 40, "adif": "40m", "itu": "HF", "mode":const.LSB}

        assert freq_to_band(10100) == {"band" : 30, "adif": "30m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(10141) == {"band" : 30, "adif": "30m", "itu": "HF", "mode":const.DIGITAL}

        assert freq_to_band(14000) == {"band" : 20, "adif": "20m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(14070) == {"band" : 20, "adif": "20m", "itu": "HF", "mode":const.DIGITAL}
        assert freq_to_band(14349) == {"band" : 20, "adif": "20m", "itu": "HF", "mode":const.USB}

        assert freq_to_band(18068) == {"band" : 17, "adif": "17m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(18096) == {"band" : 17, "adif": "17m", "itu": "HF", "mode":const.DIGITAL}
        assert freq_to_band(18250) == {"band" : 17, "adif": "17m", "itu": "HF", "mode":const.USB}

        assert freq_to_band(21000) == {"band" : 15, "adif": "15m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(21070) == {"band" : 15, "adif": "15m", "itu": "HF", "mode":const.DIGITAL}
        assert freq_to_band(21449) == {"band" : 15, "adif": "15m", "itu": "HF", "mode":const.USB}

        assert freq_to_band(24890) == {"band" : 12, "adif": "12m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(24916) == {"band" : 12, "adif": "12m", "itu": "HF", "mode":const.DIGITAL}
        assert freq_to_band(24965) == {"band" : 12, "adif": "12m", "itu": "HF", "mode":const.USB}

        assert freq_to_band(28000) == {"band" : 10, "adif": "10m", "itu": "HF", "mode":const.CW}
        assert freq_to_band(28070) == {"band" : 10, "adif": "10m", "itu": "HF", "mode":const.DIGITAL}
        assert freq_to_band(28500) == {"band" : 10, "adif": "10m", "itu": "HF", "mode":const.USB}

    def test_vhf_frequencies(self):
        assert freq_to_band(41000) == {"band" : 8, "adif": "8m", "itu": "VHF", "mode": None}

        assert freq_to_band(50000) == {"band" : 6, "adif": "6m", "itu": "VHF", "mode":const.CW}
        assert freq_to_band(50100) == {"band" : 6, "adif": "6m", "itu": "VHF", "mode":const.USB}
        assert freq_to_band(50500) == {"band" : 6, "adif": "6m", "itu": "VHF", "mode":const.DIGITAL}

        assert freq_to_band(70001) == {"band" : 4, "adif": "4m", "itu": "VHF", "mode":None}

        assert freq_to_band(144000) == {"band" : 2, "adif": "2m", "itu": "VHF", "mode":const.CW}
        assert freq_to_band(144150) == {"band" : 2, "adif": "2m", "itu": "VHF", "mode":const.USB}
        assert freq_to_band(144400) == {"band" : 2, "adif": "2m", "itu": "VHF", "mode":None}

        assert freq_to_band(220000) == {"band" : 1.25, "adif": "1.25m", "itu": "VHF", "mode":None}

    def test_uhf_frequencies(self):
        assert freq_to_band(420000) == {"band" : 0.7, "adif": "70cm", "itu": "UHF", "mode":None}

        assert freq_to_band(902000) == {"band" : 0.33, "adif": "33cm", "itu": "UHF", "mode":None}

        assert freq_to_band(1200000) == {"band" : 0.23, "adif": "23cm", "itu": "UHF", "mode":None}

        assert freq_to_band(2320200) == {"band" : 0.13, "adif": "13cm", "itu": "UHF", "mode":None}
        assert freq_to_band(2390000) == {"band" : 0.13, "adif": "13cm", "itu": "UHF", "mode":None}

    def test_shf_frequencies(self):

        assert freq_to_band(3300000) == {"band" : 0.09, "adif": "9cm", "itu": "SHF", "mode":None}

        assert freq_to_band(5650000) == {"band" : 0.053, "adif": "6cm", "itu": "SHF", "mode":None}

        assert freq_to_band(10000000) == {"band" : 0.03, "adif": "3cm", "itu": "SHF", "mode":None}

        assert freq_to_band(24000000) == {"band" : 0.0125, "adif": "1.25cm", "itu": "SHF", "mode":None}

        with pytest.raises(KeyError):
            freq_to_band(16304)

    def test_ehf_frequencies(self):
        assert freq_to_band(47000000) == {"band" : 0.0063, "adif": "6mm", "itu": "EHF", "mode":None}

        assert freq_to_band(76000000) == {"band" : 0.004, "adif": "4mm", "itu": "EHF", "mode":None}

        assert freq_to_band(122800000) == {"band" : 0.0025, "adif": "2.5mm", "itu": "EHF", "mode":None}

        assert freq_to_band(138800000) == {"band" : 0.002, "adif": "2mm", "itu": "EHF", "mode":None}

        assert freq_to_band(242800000) == {"band" : 0.001, "adif": "1mm", "itu": "EHF", "mode":None}

    def test_ft_frequencies(self):
        assert freq_to_band(1840) == {"band": 160, "adif": "160m", "itu": "MF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(3573) == {"band": 80, "adif": "80m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(7074) == {"band": 40, "adif": "40m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(10136) == {"band": 30, "adif": "30m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(14074) == {"band": 20, "adif": "20m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(18100) == {"band": 17, "adif": "17m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(21074) == {"band": 15, "adif": "15m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(24915) == {"band": 12, "adif": "12m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(28074) == {"band": 10, "adif": "10m", "itu": "HF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(50313) == {"band": 6, "adif": "6m", "itu": "VHF", "mode": const.DIGITAL} #FT8
        assert freq_to_band(144174.5) == {"band": 2, "adif": "2m", "itu": "VHF", "mode": const.DIGITAL} #FT8
