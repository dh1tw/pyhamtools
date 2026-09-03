from pyhamtools.consts import LookupConventions as const


def freq_to_band(freq):
    """converts a Frequency [kHz] into the band and mode according to the IARU bandplan

        Args:
            frequency (float): Frequency in kHz

        Returns:
            dict: Dictionary containing the band (int), adif_band (str), itu (str) and mode (str)

        Raises:
            KeyError: Wrong frequency or out of band

        Example:
           The following example converts the frequency *14005.3 kHz* into band and mode.

           >>> from pyhamtools.utils import freq_to_band
           >>> print(freq_to_band(14005.3))
           {
                'band': 20,
                'adif': '20m',
                'itu': 'HF',
                'mode': 'CW'
           }

        Note:

            Modes are:

                - CW
                - USB
                - LSB
                - DIGITAL

    """

    band = None
    adif = None
    itu = None
    mode = None
    if ((freq >= 135) and (freq <= 138)):
        band = 2190
        adif = "2190m"
        itu = "LF"
        mode = const.CW
    elif ((freq >= 472 ) and (freq <= 479)):
        band = 630
        adif = "630m"
        itu = "MF"
    elif ((freq >= 501 ) and (freq <= 504)):
        band = 560
        adif = "560m"
        itu = "MF"
    elif ((freq >= 1800) and (freq <= 2000)):
        band = 160
        adif = "160m"
        itu = "MF"
        if ((freq >= 1800) and (freq < 1838)):
            mode = const.CW
        elif ((freq >= 1838) and (freq < 1840)):
            mode = const.DIGITAL
        elif (freq == 1840):
            mode = const.DIGITAL #FT8
        elif ((freq > 1840) and (freq < 2000)):
            mode = const.LSB
    elif ((freq >= 3500) and (freq <= 4000)):
        band = 80
        adif = "80m"
        itu = "HF"
        if ((freq >= 3500) and (freq < 3573)):
            mode = const.CW
        elif (freq == 3573):
            mode = const.DIGITAL #FT8
        elif ((freq > 3573) and (freq < 3580)):
            mode = const.CW
        elif ((freq >= 3580) and (freq < 3600)):
            mode = const.DIGITAL
        elif ((freq >= 3600) and (freq < 4000)):
            mode = const.LSB
    elif ((freq >= 5000) and (freq <= 5500)):
        band = 60
        adif = "60m"
        itu = "HF"
    elif ((freq >= 7000) and (freq <= 7300)):
        band = 40
        adif = "40m"
        itu = "HF"
        if ((freq >= 7000) and (freq < 7040)):
            mode = const.CW
        elif ((freq >= 7040) and (freq < 7050)):
            mode = const.DIGITAL
        elif ((freq >= 7050) and (freq < 7074)):
            mode = const.LSB
        elif (freq == 7074):
            mode = const.DIGITAL #FT8
        elif ((freq > 7074) and (freq < 7300)):
            mode = const.LSB
    elif ((freq >= 10100) and (freq <= 10150)):
        band = 30
        adif = "30m"
        itu = "HF"
        if ((freq >= 10100) and (freq < 10136)):
            mode = const.CW
        elif (freq == 10136):
            mode = const.DIGITAL #FT8
        elif ((freq > 10136) and (freq < 10140)):
            mode = const.CW
        elif ((freq >= 10140) and (freq < 10150)):
            mode = const.DIGITAL
    elif ((freq >= 14000) and (freq <= 14350)):
        band = 20
        adif = "20m"
        itu = "HF"
        if ((freq >= 14000) and (freq < 14070)):
            mode = const.CW
        elif ((freq >= 14070) and (freq < 14074)):
            mode = const.DIGITAL
        elif (freq == 14074):
            mode = const.DIGITAL #FT8
        elif ((freq > 14074) and (freq < 14099)):
            mode = const.DIGITAL
        elif ((freq >= 14100) and (freq < 14350)):
            mode = const.USB
    elif ((freq >= 18068) and (freq <= 18268)):
        band = 17
        adif = "17m"
        itu = "HF"
        if ((freq >= 18068) and (freq < 18095)):
            mode = const.CW
        elif ((freq >= 18095) and (freq < 18100)):
            mode = const.DIGITAL
        elif (freq == 18100):
            mode = const.DIGITAL #FT8
        elif ((freq > 18100) and (freq < 18110)):
            mode = const.DIGITAL
        elif ((freq >= 18110) and (freq < 18268)):
            mode = const.USB
    elif ((freq >= 21000) and (freq <= 21450)):
        band = 15
        adif = "15m"
        itu = "HF"
        if ((freq >= 21000) and (freq < 21070)):
            mode = const.CW
        elif ((freq >= 21070) and (freq < 21074)):
            mode = const.DIGITAL
        elif (freq == 21074):
            mode = const.DIGITAL #FT8
        elif ((freq > 21074) and (freq < 21150)):
            mode = const.DIGITAL
        elif ((freq >= 21150) and (freq < 21450)):
            mode = const.USB
    elif ((freq >= 24890) and (freq <= 24990)):
        band = 12
        adif = "12m"
        itu = "HF"
        if ((freq >= 24890) and (freq < 24915)):
            mode = const.CW
        elif (freq == 24915):
            mode = const.DIGITAL #FT8
        elif ((freq > 24915) and (freq < 24930)):
            mode = const.DIGITAL
        elif ((freq >= 24930) and (freq < 24990)):
            mode = const.USB
    elif ((freq >= 28000) and (freq <= 29700)):
        band = 10
        adif = "10m"
        itu = "HF"
        if ((freq >= 28000) and (freq < 28070)):
            mode = const.CW
        elif ((freq >= 28070) and (freq < 28074)):
            mode = const.DIGITAL
        elif (freq == 28074):
            mode = const.DIGITAL #FT8
        elif ((freq > 28074) and (freq < 28190)):
            mode = const.DIGITAL
        elif ((freq >= 28300) and (freq < 29700)):
            mode = const.USB
    elif ((freq >= 40000) and (freq <= 45000)):
        band = 8 # not yet official band
        adif = "8m" # not yet official band
        itu = "VHF"
    elif ((freq >= 50000) and (freq <= 54000)):
        band = 6
        adif = "6m"
        itu = "VHF"
        if ((freq >= 50000) and (freq < 50100)):
            mode = const.CW
        elif ((freq >= 50100) and (freq < 50313)):
            mode = const.USB
        elif (freq == 50313):
            mode = const.DIGITAL #FT8
        elif ((freq > 50313) and (freq < 50500)):
            mode = const.USB
        elif ((freq >= 50500) and (freq < 51000)):
            mode = const.DIGITAL
    elif ((freq >= 70000) and (freq <= 71000)):
        band = 4
        adif = "4m"
        itu = "VHF"
        mode = None
    elif ((freq >= 144000) and (freq <= 148000)):
        band = 2
        adif = "2m"
        itu = "VHF"
        if ((freq >= 144000) and (freq < 144150)):
            mode = const.CW
        elif ((freq >= 144150) and (freq < 144174)):
            mode = const.USB
        elif (freq >= 144174) and (freq < 144175):
            mode = const.DIGITAL #FT8
        elif ((freq > 144175) and (freq < 144400)):
            mode = const.USB
        elif ((freq >= 144400) and (freq < 148000)):
            mode = None
    elif ((freq >= 220000) and (freq <= 226000)):
        band = 1.25  #1.25m
        adif = "1.25m"
        itu = "VHF"
        mode = None
    elif ((freq >= 420000) and (freq <= 470000)):
        band = 0.7  #70cm
        adif = "70cm"
        itu = "UHF"
        mode = None
    elif ((freq >= 902000) and (freq <= 928000)):
        band = 0.33  #33cm US
        adif = "33cm"
        itu = "UHF"
        mode = None
    elif ((freq >= 1200000) and (freq <= 1300000)):
        band = 0.23  #23cm
        adif = "23cm"
        itu = "UHF"
        mode = None
    elif ((freq >= 2300000) and (freq <= 2450000)):
        band = 0.13  #13cm
        adif = "13cm"
        itu = "UHF"
        mode = None
    elif ((freq >= 3300000) and (freq <= 3500000)):
        band = 0.09  #9cm
        adif = "9cm"
        itu = "SHF"
        mode = None
    elif ((freq >= 5650000) and (freq <= 5925000)):
        band = 0.053  #5.3cm
        adif = "6cm"
        itu = "SHF"
        mode = None
    elif ((freq >= 10000000) and (freq <= 10500000)):
        band = 0.03  #3cm
        adif = "3cm"
        itu = "SHF"
        mode = None
    elif ((freq >= 24000000) and (freq <= 24250000)):
        band = 0.0125  #1,25cm
        adif = "1.25cm"
        itu = "SHF"
        mode = None
    elif ((freq >= 47000000) and (freq <= 47200000)):
        band = 0.0063  #6,3mm
        adif = "6mm"
        itu = "EHF"
        mode = None
    elif ((freq >= 75500000) and (freq <= 81500000)):
        band = 0.004  #4mm
        adif = "4mm"
        itu = "EHF"
        mode = None
    elif ((freq >= 122250000) and (freq <= 123000000)):
        band = 0.0025  #2.5mm
        adif = "2.5mm"
        itu = "EHF"
        mode = None
    elif ((freq >= 134000000) and (freq <= 141000000)):
        band = 0.002  #2mm
        adif = "2mm"
        itu = "EHF"
        mode = None
    elif ((freq >= 241000000) and (freq <= 250000000)):
        band = 0.001  #1mm
        adif = "1mm"
        itu = "EHF"
        mode = None
    else:
        raise KeyError

    return {"band": band, "adif": adif, "itu": itu, "mode": mode}
