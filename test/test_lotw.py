import os
import sys
import datetime

from past.builtins import execfile
from future.utils import iteritems
import pytest

from pyhamtools.qsl import get_lotw_users

if sys.version_info.major == 3:
    unicode = str

test_dir = os.path.dirname(os.path.abspath(__file__))
fix_dir = os.path.join(test_dir, 'fixtures')

class Test_lotw_methods:

    def test_check_content_with_mocked_http_server(self, httpserver):
        httpserver.serve_content(open(os.path.join(fix_dir, 'lotw-user-activity.csv')).read())

        namespace = {}
        execfile(os.path.join(fix_dir,"lotw_fixture.py"), namespace)
        assert get_lotw_users(url=httpserver.url) == namespace['lotw_fixture']

    def test_download_lotw_list_and_check_types(self):

        data = get_lotw_users()
        assert isinstance(data, dict)
        for key, value in iteritems(data):
            assert isinstance(key, unicode)
            assert isinstance(value, datetime.datetime )
        assert len(data) > 1000

    def test_with_invalid_url(self):
        with pytest.raises(IOError):
            get_lotw_users(url="https://lotw.arrl.org/lotw-user-activity_FAKE.csv")

    def test_with_more_than_10_invalid_dates(self, httpserver):
        httpserver.serve_content(open(os.path.join(fix_dir, 'lotw_data_with_errors.html')).read())

        with pytest.raises(ValueError):
            get_lotw_users(url=httpserver.url)


