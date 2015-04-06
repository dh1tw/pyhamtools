import os 
import datetime

import pytest

from pyhamtools.qsl import get_eqsl_users

class Test_eqsl_methods:

    def test_check_content_with_mocked_http_server(self, httpserver):
        httpserver.serve_content(open('./fixtures/eqsl_data.html').read(), headers={'content-type': 'text/plain; charset=ISO-8859-1'})

        exec(open(os.path.join("./fixtures/","eqsl_data.py")).read())
        assert get_eqsl_users(url=httpserver.url) == eqsl_fixture

    def test_download_lotw_list_and_check_types(self):

        data = get_eqsl_users()
        assert isinstance(data, list)
        for el in data:
            assert isinstance(el, unicode)
        assert len(data) > 1000

    def test_with_invalid_url(self):
        with pytest.raises(IOError):
            get_eqsl_users(url="http://www.eqsl.cc/QSLCard/DownloadedFiles/AGMemberlist_my_unit_test.txt")