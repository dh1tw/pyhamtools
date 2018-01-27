import pytest
import os
from datetime import datetime

from pyhamtools.lookuplib import LookupLib
from pyhamtools.exceptions import APIKeyMissingError

#Fixtures
#===========================================================

response_Prefix_DH = {
          'adif': 230,
          'country': 'Fed. Rep. of Germany',
          'continent': 'EU',
          'latitude': 51.0,
          'longitude': 10.0,
          'cqz': 14,
          'ituz' : 28
        }


response_Exception_3D2RI = {
          'adif': 460,
          'country': 'Rotuma Island',
          'continent': 'OC',
          'latitude': -12.48,
          'longitude': 177.08,
          'cqz': 32,
          'ituz' : 56
        }

@pytest.fixture(scope="function")
def fix_plist_file(request):
    dir = os.path.dirname(__file__)
    cty_file_rel = "./fixtures/cty.plist"
    cty_file_abs = os.path.join(dir, cty_file_rel)
    return cty_file_abs


#TESTS
#===========================================================

#@pytest.mark.skipif(True, reason="slow test")
class Test_Countryfile_Constructor:

    def test_constructor_with_file_instead_of_downlad(self, fix_plist_file):
        lib = LookupLib("countryfile", filename=fix_plist_file)
        assert lib.lookup_callsign("3D2RI") == response_Exception_3D2RI


    def test_constructor_with_invalid_file(self):
        with pytest.raises(IOError):
            lib = LookupLib("countryfile", filename="foo bar")
            lib.lookup_callsign("GB0BVL")

class Test_countryfile_Getter_Setter:

    #lookup_entity(adif)
    #===============================
    def test_getException(self, fixCountryFile):
        with pytest.raises(KeyError):
            fixCountryFile.lookup_entity(230)


    #lookup_callsign(callsign, [date])
    #===============================
    def test_getException(self, fixCountryFile):
        assert fixCountryFile.lookup_callsign("3D2RI") == response_Exception_3D2RI

        with pytest.raises(KeyError):
            fixCountryFile.lookup_callsign("QRM")

        with pytest.raises(KeyError):
            fixCountryFile.lookup_callsign("")


    #lookup_prefix(prefix, [date])
    #=========================
    def test_lookup_prefix(self, fixCountryFile):
        assert fixCountryFile.lookup_prefix("DH") == response_Prefix_DH

        with pytest.raises(KeyError):
            fixCountryFile.lookup_prefix("QRM")

        with pytest.raises(KeyError):
            fixCountryFile.lookup_prefix("")

    #is_invalid_operation(callsign, [date])
    #===============================
    def test_is_invalid_operation(self, fixCountryFile):
        with pytest.raises(KeyError):
            fixCountryFile.is_invalid_operation("5W1CFN")

    #lookup_zone_exception(callsign, [date])
    #====================================
    def test_lookup_zone_exception(self, fixCountryFile):
        with pytest.raises(KeyError):
            fixCountryFile.lookup_zone_exception("dp0gvn")