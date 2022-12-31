import pytest
import pkgutil
import json

from pyhamtools import LookupLib
from pyhamtools import Callinfo

APIKEY = ""
QRZ_USERNAME = ""
QRZ_PWD = ""

try:
    APIKEY = str(os.environ['CLUBLOG_APIKEY'])
    QRZ_USERNAME = str(os.environ['QRZ_USERNAME'])
    QRZ_PWD = str(os.environ['QRZ_PWD'])

except Exception as ex:
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
    Lib = LookupLib(request.param, fixApiKey)
    # pytest.skip("better later")
    return(Lib)

@pytest.fixture(scope="module")
def fixClublogApi(request, fixApiKey):
    Lib = LookupLib("clublogapi", fixApiKey)
    return(Lib)

@pytest.fixture(scope="module")
def fixClublogXML(request, fixApiKey):
    Lib = LookupLib("clublogxml", fixApiKey)
    return(Lib)

@pytest.fixture(scope="module")
def fixCountryFile(request):
    Lib = LookupLib("countryfile")
    return(Lib)

@pytest.fixture(scope="module", params=["clublogxml", "countryfile"])
def fix_callinfo(request, fixApiKey):
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
    return LookupLib(lookuptype="qrz", username=QRZ_USERNAME, pwd=QRZ_PWD)

@pytest.fixture(scope="session")
def fixCountryMapping():
        return json.loads(pkgutil.get_data("pyhamtools", "countryfilemapping.json"))