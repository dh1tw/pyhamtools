from __future__ import unicode_literals
import pytest
import tempfile
import os
import sys

if sys.version_info.major == 3:
    unicode = str

from datetime import datetime

#Fixtures
#===========================================================


@pytest.fixture(scope="function", params=[112, 5, "", "dh1tw", 11.5, -5, {}, []])
def fixEntities(request):
    return request.param

@pytest.fixture(scope="function", params=["dh1tw", "VE9ST/NA14", "VA3RLG/PM", "", 5, 12.5, -9999, {}, []])
def fixExceptions(request):
    return request.param

@pytest.fixture(scope="function", params=["DH", "DH1TW", "", 5, 12.5, -9999, {}, []])
def fixPrefixes(request):
    return request.param

@pytest.fixture(scope="function", params=["DH1TW", "JA3UB/GAZA", "", 5, 12.5, -9999, {}, []])
def fixInvalidOperations(request):
    return request.param

@pytest.fixture(scope="function", params=["DH1TW", "ve8ev", "", 5, 12.5, -9999, {}, []])
def fixZoneExceptions(request):
    return request.param

@pytest.fixture(scope="function", params=[{"DH1TW": {'latitude': 51.0, 'country': 'FEDERAL REPUBLIC OF GERMANY',
                                'continent': 'EU', 'longitude': -10.0, 'cqz': 14}}, {}, "ve8ev", "", 5, 12.5, -9999])
def fixSetExceptions(request):
    return request.param



#TESTS
#===========================================================

class Test_Getter_Setter_Api_Types_for_all_sources:

    def test_lookup_entity_without_entity_nr(self, fixGeneralApi):
        with pytest.raises(Exception):
            fixGeneralApi.lookup_entity()

    def test_lookup_entity(self, fixGeneralApi, fixEntities):
        try:
            entity = fixGeneralApi.lookup_entity(fixEntities)

            assert type(entity) is dict
            if len(entity) > 0:
                count = 0
                for attr in entity:
                    if attr == "country":
                        assert type(entity[attr] is unicode)
                        count +=1
                    if attr == "continent":
                        assert type(entity[attr] is unicode)
                        count +=1
                    if attr == "prefix":
                        assert type(entity[attr] is unicode)
                        count +=1
                    if attr == "deleted":
                        assert type(entity[attr] is bool)
                        count +=1
                    if attr == "cqz":
                        assert type(entity[attr] is int)
                        count +=1
                    if attr == "longitude":
                        assert type(entity[attr] is float)
                        count +=1
                    if attr == "latitude":
                        assert type(entity[attr] is float)
                        count +=1
                    if attr == "start":
                        assert type(entity[attr] is datetime)
                        count +=1
                    if attr == "end":
                        assert type(entity[attr] is datetime)
                        count +=1
                    if attr == "whitelist":
                        assert type(entity[attr] is bool)
                        count +=1
                    if attr == "whitelist_start":
                        assert type(entity[attr] is datetime)
                        count +=1
                    if attr == "whitelist_end":
                        assert type(entity[attr] is datetime)
                        count +=1
                assert len(entity) == count
        except KeyError:
            pass
        except TypeError:
            pass
        except ValueError:
            pass

    def test_lookup_callsign(self, fixGeneralApi, fixExceptions):
        try:
            ex = fixGeneralApi.lookup_callsign(fixExceptions)
            assert type(ex) is dict
            count = 0
            for attr in ex:
                if attr == "latitude":
                        assert type(ex[attr]) is float
                        count +=1
                elif attr == "longitude":
                        assert type(ex[attr]) is float
                        count +=1
                elif attr == "country":
                        assert type(ex[attr]) is unicode
                        count +=1
                elif attr == "continent":
                        assert type(ex[attr]) is unicode
                        count +=1
                elif attr == "cqz":
                        assert type(ex[attr]) is int
                        count +=1
                elif attr == "ituz":
                        assert type(ex[attr]) is int
                        count +=1
                elif attr == "start":
                        assert type(ex[attr]) is datetime
                        count +=1
                elif attr == "end":
                        assert type(ex[attr]) is datetime
                        count +=1
                elif attr == "adif":
                        assert type(ex[attr]) is int
                        count +=1

            #all attributes checked?
            assert len(ex) == count
        except KeyError:
            pass
        except AttributeError:
            pass

    def test_lookup_prefix(self, fixGeneralApi, fixPrefixes):

        try:
            prefix = fixGeneralApi.lookup_prefix(fixPrefixes)
            assert type(prefix) is dict
            count = 0
            for attr in prefix:
                if attr == "country":
                        assert type(prefix[attr]) is unicode
                        count +=1
                elif attr == "adif":
                        assert type(prefix[attr]) is int
                        count +=1
                elif attr == "cqz":
                        assert type(prefix[attr]) is int
                        count +=1
                elif attr == "ituz":
                        assert type(prefix[attr]) is int
                        count +=1
                elif attr == "continent":
                        assert type(prefix[attr]) is unicode
                        count +=1
                elif attr == "latitude":
                        assert type(prefix[attr]) is float
                        count +=1
                elif attr == "longitude":
                        assert type(prefix[attr]) is float
                        count +=1
                elif attr == "start":
                        assert type(prefix[attr]) is datetime
                        count +=1
                elif attr == "end":
                        assert type(prefix[attr]) is datetime
                        count +=1

            #all attributes checked?
            assert len(prefix) == count
        except KeyError:
            pass
        except AttributeError:
            pass


    def test_get_InvalidOperation(self, fixGeneralApi, fixInvalidOperations):
        try:
            invOp = fixGeneralApi.is_invalid_operation(fixInvalidOperations)
            assert type(invOp) is bool
        except KeyError:
            pass
        except AttributeError:
            pass

    def test_get_ZoneException(self, fixGeneralApi, fixZoneExceptions):
        try:
            zEx = fixGeneralApi.lookup_zone_exception(fixZoneExceptions)
            assert type(zEx) is int
        except KeyError:
            pass
        except AttributeError:
            pass

    def test_set_Exception(self, fixGeneralApi, fixSetExceptions):
        try:
            response = fixGeneralApi.setException(fixSetExceptions)
            assert type(response) is bool
            assert fixGeneralApi.lookup_callsign(fixSetExceptions.keys()[0]) == fixSetExceptions[fixSetExceptions.keys()[0]]
        except KeyError:
            pass
        except AttributeError:
            pass
