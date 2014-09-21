import pytest
from datetime import datetime


import pytz


from pyhamtools.consts import LookupConventions as const
from pyhamtools.dxcluster import decode_char_spot, decode_pc11_message, decode_pc61_message

UTC = pytz.UTC

fix_spot1 = "DX de CT3FW:     21004.8  HC2AO        599 TKS(CW)QSL READ,QRZ.COM    2132Z"
fix_spot1_broken_spotter_call = "DX de $QRM:     21004.8  HC2AO        599 TKS(CW)QSL READ,QRZ.COM    2132Z"

fix_spot_pc11 = "PC11^14010.0^R155AP^30-Apr-2014^2252Z^CQ CQ^R9CAC^RN6BN^H95^~"
fix_spot_pc61 = "PC61^14030.5^ZF2NUE^30-Apr-2014^2253Z^ ^ND4X^W4NJA^72.51.152.150^H96^~"

fix_spot2 = "DX de DL6NAA: 10368887.0  DL7VTX/B     55s in JO50VFjo62 never hrd B4 1505Z"
fix_spot3 = "DX de CT3FW:     21004.8  IDIOT        599 TKS(CW)QSL READ,QRZ.COM    2132Z"
fix_spot4 = "DX de OK1TEH:   144000.0  C0NTEST      -> www.darkside.cz/qrv.php     1328Z JO70"
fix_spot5 = "DX de DK7UK:     50099.0  EA5/ON4CAU   JN48QT<ES>IM98 QRP 5W LOOP ANT 1206Z"
fix_spot6 = "DX de UA3ZBK:    14170.0  UR8EW/QRP    POWER 2-GU81+SPYDER            1211Z"
fix_spot7 = "DX de 9K2/K2SES  14205.0  DK0HY                                       0921Z" #missing semicolon
fix_spot8 = "DX de DK1CS:9330368887.0  DL7VTX/B                                    1505Z"
fix_spot9 = "DX de DH1TW:        23.0  DS1TW                                       1505Z"
fix_spot10 = "DX de DH1TW    234.0  DS1TW                                          1505Z"
fix_spot11 = "DX de DH1TW:       234.0  DS1TW                                       1505Z"
fix_spot12 = "DX de DH1TW:     50105.0  ZD6DYA                                      1505Z"

response_spot1 = {
    const.SPOTTER: "CT3FW",
    const.DX: "HC2AO",
    const.BAND: 15,
    const.MODE: "CW",
    const.COMMENT: "599 TKS(CW)QSL READ,QRZ.COM",
    const.TIME: datetime.utcnow().replace( hour=21, minute=32, second=0, microsecond = 0, tzinfo=UTC)
}


class TestDXClusterSpots:

    def test_spots(self):
        assert decode_char_spot(fix_spot1)[const.SPOTTER] == "CT3FW"
        assert decode_char_spot(fix_spot1)[const.DX] == "HC2AO"
        assert decode_char_spot(fix_spot1)[const.FREQUENCY] == 21004.8
        assert decode_char_spot(fix_spot1)[const.COMMENT] == "599 TKS(CW)QSL READ,QRZ.COM"
        assert isinstance(decode_char_spot(fix_spot1)[const.TIME], datetime)

        with pytest.raises(ValueError):
            decode_char_spot(fix_spot1_broken_spotter_call)


    def test_spots_pc11(self):
        assert decode_pc11_message(fix_spot_pc11)[const.SPOTTER] == "R9CAC"
        assert decode_pc11_message(fix_spot_pc11)[const.DX] == "R155AP"
        assert decode_pc11_message(fix_spot_pc11)[const.FREQUENCY] == 14010.0
        assert decode_pc11_message(fix_spot_pc11)[const.COMMENT] == "CQ CQ"
        assert decode_pc11_message(fix_spot_pc11)["node"] == "RN6BN"
        assert isinstance(decode_pc11_message(fix_spot_pc11)[const.TIME], datetime)

    def test_spots_pc61(self):
        assert decode_pc61_message(fix_spot_pc61)[const.SPOTTER] == "ND4X"
        assert decode_pc61_message(fix_spot_pc61)[const.DX] == "ZF2NUE"
        assert decode_pc61_message(fix_spot_pc61)[const.FREQUENCY] == 14030.5
        assert decode_pc61_message(fix_spot_pc61)[const.COMMENT] == " "
        assert decode_pc61_message(fix_spot_pc61)["node"] == "W4NJA"
        assert decode_pc61_message(fix_spot_pc61)["ip"] == "72.51.152.150"
        assert isinstance(decode_pc61_message(fix_spot_pc61)[const.TIME], datetime)