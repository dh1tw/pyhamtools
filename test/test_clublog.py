import os
import sys
import datetime

import pytest
from future.utils import iteritems

from pyhamtools.qsl import get_clublog_users

if sys.version_info.major == 3:
    unicode = str

test_dir = os.path.dirname(os.path.abspath(__file__))
fix_dir = os.path.join(test_dir, 'fixtures')

class Test_clublog_methods:

    def test_check_content_with_mocked_http_server(self, httpserver):
        httpserver.serve_content(
            open(os.path.join(fix_dir, 'clublog-users.json.zip'), 'rb').read())

        data = get_clublog_users(url=httpserver.url)
        assert len(data) == 139081

    def test_download_lotw_list_and_check_types(self):

        data = get_clublog_users()
        assert isinstance(data, dict)
        for key, value in iteritems(data):
            assert isinstance(key, unicode)
            assert isinstance(value, dict)

    def test_with_invalid_url(self):
        with pytest.raises(IOError):
            get_clublog_users(url="https://FAKE.csv")
