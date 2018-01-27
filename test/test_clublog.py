import os
import datetime

import pytest

from pyhamtools.qsl import get_clublog_users


class Test_clublog_methods:

    def test_check_content_with_mocked_http_server(self, httpserver):
        httpserver.serve_content(
            open('./fixtures/clublog-users.json.zip').read())

        data = get_clublog_users(url=httpserver.url)
        assert len(data) == 139081

    def test_download_lotw_list_and_check_types(self):

        data = get_clublog_users()
        assert isinstance(data, dict)
        for key, value in data.iteritems():
            assert isinstance(key, unicode)
            assert isinstance(value, dict)

    def test_with_invalid_url(self):
        with pytest.raises(IOError):
            get_clublog_users(url="https://FAKE.csv")
