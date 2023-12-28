import pytest
import json
from datetime import datetime, timezone

import redis

from pyhamtools import LookupLib, Callinfo

r = redis.Redis()


response_Exception_VP8STI_with_start_and_stop_date = {
           'adif': 240,
           'country': u'SOUTH SANDWICH ISLANDS',
           'continent': u'SA',
           'latitude': -59.48,
           'longitude': -27.29,
           'cqz': 13,
        }

response_TU5PCT = {
           'adif': 428,
           'country': u"COTE D'IVOIRE",
           'continent': u'AF',
           'latitude': 5.3,
           'longitude': -4.0,
           'cqz': 35,
        }

class TestStoreDataInRedis:

    def test_copy_data_in_redis(self, fixClublogXML, fix_redis):

        fixClublogXML.copy_data_in_redis("clx", redis.Redis())
        assert fix_redis.lookup_entity(280) == fixClublogXML.lookup_entity(280)
        assert fix_redis.lookup_callsign("VK9XO") == fixClublogXML.lookup_callsign("VK9XO")
        assert fix_redis.lookup_prefix("DH") == fixClublogXML.lookup_prefix("DH")


        with pytest.raises(KeyError):
            fix_redis.is_invalid_operation("VK0MC")

        timestamp = datetime(year=1994, month=12, day=30, tzinfo=timezone.utc)
        assert fix_redis.is_invalid_operation("VK0MC", timestamp)

        with pytest.raises(KeyError):
            fix_redis.lookup_zone_exception("DH1TW")

        assert fix_redis.lookup_zone_exception("dp0gvn") == 38


    def test_copy_data_in_redis_2(self, fixCountryFile):

        lib = LookupLib(lookuptype="redis", redis_prefix="CF", redis_instance=r)
        fixCountryFile.copy_data_in_redis("CF", r)
        assert lib.lookup_callsign("3D2RI") == fixCountryFile.lookup_callsign("3D2RI")
        assert lib.lookup_prefix("DH") == fixCountryFile.lookup_prefix("DH")

    def test_redis_lookup(self, fixClublogXML, fix_redis):
        timestamp = datetime(year=2016, month=1, day=20, tzinfo=timezone.utc)
        ci = Callinfo(fix_redis)
        assert ci.get_all("VP8STI", timestamp) == response_Exception_VP8STI_with_start_and_stop_date
        assert ci.get_all("tu5pct") == response_TU5PCT
