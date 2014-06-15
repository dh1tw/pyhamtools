import pytest
import json
from datetime import datetime

import pytz
import redis

from pyhamtools import LookupLib


UTC = pytz.UTC

r = redis.Redis()


class TestStoreDataInRedis:

    def test_copy_data_in_redis(self, fixClublogXML, fix_redis):

        fixClublogXML.copy_data_in_redis("clx", redis.Redis())
        assert fix_redis.lookup_entity(280) == fixClublogXML.lookup_entity(280)
        assert fix_redis.lookup_callsign("VK9XO") == fixClublogXML.lookup_callsign("VK9XO")
        assert fix_redis.lookup_prefix("DH") == fixClublogXML.lookup_prefix("DH")

        with pytest.raises(KeyError):
            fix_redis.is_invalid_operation("VK0MC")

        timestamp = datetime(year=1994, month=12, day=30).replace(tzinfo=UTC)
        assert fix_redis.is_invalid_operation("VK0MC", timestamp)

        with pytest.raises(KeyError):
            fix_redis.lookup_zone_exception("DH1TW")

        assert fix_redis.lookup_zone_exception("dp0gvn") == 38


    def test_copy_data_in_redis_2(self, fixCountryFile):

        lib = LookupLib(lookuptype="redis", redis_prefix="CF", redis_instance=r)
        fixCountryFile.copy_data_in_redis("CF", r)
        assert lib.lookup_callsign("3D2RI") == fixCountryFile.lookup_callsign("3D2RI")
        assert lib.lookup_prefix("DH") == fixCountryFile.lookup_prefix("DH")