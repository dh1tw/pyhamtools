import pytest
from datetime import datetime

from pyhamtools.lookuplib import LookupLib
from pyhamtools.exceptions import APIKeyMissingError, NoResult, LookupError

#Fixtures
#===========================================================

response_Prefix_DH = { 
          'adif': 230, 
          'country': 'Fed. Rep. of Germany', 
          'continent': 'EU', 
          'latitude': 51.0, 
          'longitude': -10.0, 
          'cqz': 14,
          'ituz' : 28
        }


response_Exception_3D2RI = { 
          'adif': 460, 
          'country': 'Rotuma Island', 
          'continent': 'OC', 
          'latitude': -12.48, 
          'longitude': -177.08, 
          'cqz': 32,
          'ituz' : 56
        }
        
@pytest.fixture(scope="function")
def fixPlistFile(request):
    return "/Users/user/projects/pyhamtools/pyhamtools/cty.plist"


#TESTS
#===========================================================

#@pytest.mark.skipif(True, reason="slow test")
class Test_Countryfile_Constructor:

    def test_object_construction_with_invalid_files(self):
        with pytest.raises(AttributeError):
            LookupLib("countryfile", download=False)
            
        with pytest.raises(AttributeError):
            LookupLib("countryfile", filename="", download=False)

        with pytest.raises(AttributeError):
            LookupLib("countryfile", filename="foo bar", download=False)




class Test_countryfile_Getter_Setter:
    
    #lookup_entity(adif)
    #===============================
    def test_getException(self, fixCountryFile):
        with pytest.raises(NoResult):
            fixCountryFile.lookup_entity(230)
    
    
    #lookup_callsign(callsign, [date])
    #===============================
    def test_getException(self, fixCountryFile):
        assert fixCountryFile.lookup_callsign("3D2RI") == response_Exception_3D2RI

        with pytest.raises(NoResult):
            fixCountryFile.lookup_callsign("QRM")

        with pytest.raises(NoResult):
            fixCountryFile.lookup_callsign("")
              
    
    #lookup_prefix(prefix, [date])
    #=========================
    def test_lookup_prefix(self, fixCountryFile):
        assert fixCountryFile.lookup_prefix("DH") == response_Prefix_DH

        with pytest.raises(NoResult):
            fixCountryFile.lookup_prefix("QRM")

        with pytest.raises(NoResult):
            fixCountryFile.lookup_prefix("")

    #is_invalid_operation(callsign, [date])
    #===============================
    def test_is_invalid_operation(self, fixCountryFile):
        with pytest.raises(NoResult):
            fixCountryFile.is_invalid_operation("5W1CFN")

    #lookup_zone_exception(callsign, [date])
    #====================================    
    def test_lookup_zone_exception(self, fixCountryFile):
        with pytest.raises(NoResult):
            fixCountryFile.lookup_zone_exception("dp0gvn")