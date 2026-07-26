import pytest
import pkgutil
import json
import os

from pyhamtools import LookupLib
from pyhamtools import Callinfo

APIKEY = str(os.getenv('CLUBLOG_APIKEY', '')).strip()
QRZ_USERNAME = str(os.getenv('QRZ_USERNAME', '')).strip()
QRZ_PWD = str(os.getenv('QRZ_PWD', '')).strip()
HAS_CLUBLOG_APIKEY = bool(APIKEY)
HAS_QRZ_CREDENTIALS = bool(QRZ_USERNAME and QRZ_PWD)

if not HAS_CLUBLOG_APIKEY or not HAS_QRZ_CREDENTIALS:
    print("WARNING: Environment variables with API keys not set; some tests will be skipped")

@pytest.fixture(scope="session", params=["a", "", 12.5, -5, {"foo" : "bar"}, [5, "foo"]])
def fixNonUnsignedInteger(request):
    return request.param

@pytest.fixture(scope="session", params=[12.5, -5, 34569, {"foo" : "bar"}, [5, "foo"]])
def fixNonString(request):
    return request.param

@pytest.fixture(scope="session", params=[12.5, -5.5, 34569.0000001])
def fixFloats(request):
    return request.param

@pytest.fixture(scope="session", params=["", "-5.5", "foo bar"])
def fixStrings(request):
    return request.param

@pytest.fixture(scope="session", params=[0, -2322321, 32321321])
def fixIntegers(request):
    return request.param

@pytest.fixture(scope="session", params=[{"foo": "bar"}, {}, {-99.99 : {"foo": 12}}])
def fixDicts(request):
    return request.param

@pytest.fixture(scope="session", params=[["foo", "bar", 99.12], [None, 55, "foo"]])
def fixLists(request):
    return request.param

@pytest.fixture(scope="session", params=[None])
def fixNone(request):
    return request.param

@pytest.fixture(scope="session")
def fixApiKey(request):
    return(APIKEY)

@pytest.fixture(scope="module", params=["clublogapi", "clublogxml", "countryfile"])
def fixGeneralApi(request, fixApiKey):
    """Fixture returning all possible instances of LookupLib"""
    if request.param in ("clublogapi", "clublogxml") and not HAS_CLUBLOG_APIKEY:
        pytest.skip("Environment variable CLUBLOG_APIKEY not set")
    if request.param == "countryfile":
        cty_file_abs = os.path.join(os.path.dirname(__file__), "./fixtures/cty.plist")
        Lib = LookupLib(request.param, fixApiKey, filename=cty_file_abs)
    else:
        Lib = LookupLib(request.param, fixApiKey)
    # pytest.skip("better later")
    return(Lib)

@pytest.fixture(scope="module")
def fixClublogApi(request, fixApiKey):
    if not HAS_CLUBLOG_APIKEY:
        pytest.skip("Environment variable CLUBLOG_APIKEY not set")
    Lib = LookupLib("clublogapi", fixApiKey)
    return(Lib)

@pytest.fixture(scope="module")
def fixClublogXML(request, fixApiKey):
    if not HAS_CLUBLOG_APIKEY:
        pytest.skip("Environment variable CLUBLOG_APIKEY not set")
    Lib = LookupLib("clublogxml", fixApiKey)
    return(Lib)

@pytest.fixture(scope="module")
def fixCountryFile(request):
    cty_file_abs = os.path.join(os.path.dirname(__file__), "./fixtures/cty.plist")
    Lib = LookupLib("countryfile", filename=cty_file_abs)
    return(Lib)

@pytest.fixture(scope="module", params=["clublogxml", "countryfile"])
def fix_callinfo(request, fixApiKey):
    if request.param == "clublogxml" and not HAS_CLUBLOG_APIKEY:
        pytest.skip("Environment variable CLUBLOG_APIKEY not set")
    if request.param == "countryfile":
        cty_file_abs = os.path.join(os.path.dirname(__file__), "./fixtures/cty.plist")
        lib = LookupLib(request.param, fixApiKey, filename=cty_file_abs)
    else:
        lib = LookupLib(request.param, fixApiKey)
    callinfo = Callinfo(lib)
    return(callinfo)

# @pytest.fixture(scope="module", params=["clublogapi", "clublogxml", "countryfile"])
# def fix_callinfo(request, fixApiKey):
#     lib = LookupLib(request.param, fixApiKey)
#     callinfo = Callinfo(lib)
#     return(callinfo)

@pytest.fixture(scope="module")
def fix_redis():
    import redis
    return LookupLib(lookuptype="redis", redis_instance=redis.Redis(), redis_prefix="clx")

@pytest.fixture(scope="module")
def fix_qrz():
    if not HAS_QRZ_CREDENTIALS:
        pytest.skip("Environment variables with QRZ.com credentials not set")
    return LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd=QRZ_PWD)

@pytest.fixture(scope="session")
def fixCountryMapping():
        return json.loads(pkgutil.get_data("pyhamtools", "countryfilemapping.json"))