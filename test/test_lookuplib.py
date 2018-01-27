from __future__ import unicode_literals
import pytest
import sys

from pyhamtools.lookuplib import LookupLib
from pyhamtools.exceptions import APIKeyMissingError

if sys.version_info.major == 3:
    unicode = str

@pytest.fixture(scope="function", params=[5, -5,  "", "foo bar", 11.5, {}, [], None, ("foo", "bar")])
def fixAnyValue(request):
    return request.param


class TestlookupLib:


    def test_construction_with_invalid_kwargs(self, fixAnyValue):
        """Load with non without any args & kwargs"""
        with pytest.raises(AttributeError):
            LookupLib(fixAnyValue)



class TestlookupLibHelper:

    # def test_checkApiKeyValidity(self, fixClublogApi, fixApiKey):
    #
    #     with pytest.raises(AttributeError):
    #         fixClublogApi._checkApiKeyValidity()
    #
    #     with pytest.raises(ValueError):
    #         fixClublogApi._checkApiKeyValidity(apikey="")
    #
    #     assert fixClublogApi._checkApiKeyValidity(apikey=fixApiKey) is True


    def test_generateRandomWord(self, fixClublogApi, fixNonUnsignedInteger):

        with pytest.raises(TypeError):
            fixClublogApi._generate_random_word()

        assert type(fixClublogApi._generate_random_word(5)) is unicode
        assert len(fixClublogApi._generate_random_word(5)) is 5
