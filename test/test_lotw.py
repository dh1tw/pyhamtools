import os
import datetime

from .execfile import execfile
import pytest

def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        "__file__": filepath,
        "__name__": "__main__",
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


from pyhamtools.qsl import get_lotw_users

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
        for key, value in data.items():
            assert isinstance(key, str)
            assert isinstance(value, datetime.datetime )
        assert len(data) > 1000

    def test_with_invalid_url(self):
        with pytest.raises(IOError):
            get_lotw_users(url="https://lotw.arrl.org/lotw-user-activity_FAKE.csv")

    def test_with_more_than_10_invalid_dates(self, httpserver):
        httpserver.serve_content(open(os.path.join(fix_dir, 'lotw_data_with_errors.html')).read())

        with pytest.raises(ValueError):
            get_lotw_users(url=httpserver.url)


