from future.utils import iteritems
from datetime import datetime
import re

import requests
import redis
import zipfile
import json
from io import BytesIO
from requests.exceptions import ConnectionError, HTTPError, Timeout

def get_lotw_users(**kwargs):
    """Download the latest offical list of `ARRL Logbook of the World (LOTW)`__ users.

        Args:
            url (str, optional): Download URL

        Returns:
            dict: Dictionary containing the callsign (unicode) date of the last LOTW upload (datetime)

        Raises:
            IOError: When network is unavailable, file can't be downloaded or processed

            ValueError: Raised when data from file can't be read

        Example:
           The following example downloads the LOTW user list and check when DH1TW has made his last LOTW upload:

           >>> from pyhamtools.qsl import get_lotw_users
           >>> mydict = get_lotw_users()
           >>> mydict['DH1TW']
           datetime.datetime(2014, 9, 7, 0, 0)

    .. _ARRL: http://www.arrl.org/logbook-of-the-world
    __ ARRL_

    """

    url = ""

    lotw = {}

    try:
        url = kwargs['url']
    except KeyError:
        # url = "http://wd5eae.org/LoTW_Data.txt"
        url = "https://lotw.arrl.org/lotw-user-activity.csv"

    try:
        result = requests.get(url)
    except (ConnectionError, HTTPError, Timeout) as e:
        raise IOError(e)

    error_count = 0

    if result.status_code == requests.codes.ok:
        for el in result.text.split():
            data = el.split(",")
            try:
                lotw[data[0]] = datetime.strptime(data[1], '%Y-%m-%d')
            except ValueError as e:
                error_count += 1
                if error_count > 10:
                    raise ValueError("more than 10 wrongly formatted datasets " + str(e))

    else:
        raise IOError("HTTP Error: " + str(result.status_code))

    return lotw

def get_clublog_users(**kwargs):
    """Download the latest offical list of `Clublog`__ users.

        Args:
            url (str, optional): Download URL

        Returns:
            dict: Dictionary containing (if data available) the fields:
                firstqso, lastqso, last-lotw, lastupload (datetime),
                locator (string) and oqrs (boolean)

        Raises:
            IOError: When network is unavailable, file can't be downloaded or processed

        Example:
           The following example downloads the Clublog user list and returns a dictionary with the data of HC2/AL1O:

           >>> from pyhamtools.qsl import get_clublog_users
           >>> clublog = get_lotw_users()
           >>> clublog['HC2/AL1O']
           {'firstqso': datetime.datetime(2012, 1, 1, 19, 59, 27),
            'last-lotw': datetime.datetime(2013, 5, 9, 1, 56, 23),
            'lastqso': datetime.datetime(2013, 5, 5, 6, 39, 3),
            'lastupload': datetime.datetime(2013, 5, 8, 15, 0, 6),
            'oqrs': True}

    .. _CLUBLOG: https://secure.clublog.org
    __ CLUBLOG_

    """

    url = ""

    clublog = {}

    try:
        url = kwargs['url']
    except KeyError:
        url = "https://secure.clublog.org/clublog-users.json.zip"

    try:
        result = requests.get(url)
    except (ConnectionError, HTTPError, Timeout) as e:
        raise IOError(e)


    if result.status_code != requests.codes.ok:
        raise IOError("HTTP Error: " + str(result.status_code))

    zip_file = zipfile.ZipFile(BytesIO(result.content))
    files = zip_file.namelist()
    cl_json_unzipped = zip_file.read(files[0]).decode('utf8').replace("'", '"')

    cl_data = json.loads(cl_json_unzipped, encoding='UTF-8')

    error_count = 0

    for call, call_data in iteritems(cl_data):
        try:
            data = {}
            if "firstqso" in call_data:
                if call_data["firstqso"] != None:
                    data["firstqso"] = datetime.strptime(call_data["firstqso"], '%Y-%m-%d %H:%M:%S')
            if "lastqso" in call_data:
                if call_data["lastqso"] != None:
                    data["lastqso"] = datetime.strptime(call_data["lastqso"], '%Y-%m-%d %H:%M:%S')
            if "last-lotw" in call_data:
                if call_data["last-lotw"] != None:
                    data["last-lotw"] = datetime.strptime(call_data["last-lotw"], '%Y-%m-%d %H:%M:%S')
            if "lastupload" in call_data:
                if call_data["lastupload"] != None:
                    data["lastupload"] = datetime.strptime(call_data["lastupload"], '%Y-%m-%d %H:%M:%S')
            if "locator" in call_data:
                if call_data["locator"] != None:
                    data["locator"] = call_data["locator"]
            if "oqrs" in call_data:
                if call_data["oqrs"] != None:
                    data["oqrs"] = call_data["oqrs"]
            clublog[call] = data
        except TypeError: #some date fields contain null instead of a valid datetime string - we ignore them
            print("Ignoring invalid type in data:", call, call_data)
            pass
        except ValueError: #some date fiels are invalid. we ignore them for the moment
            print("Ignoring invalid data:", call, call_data)
            pass

    return clublog

def get_eqsl_users(**kwargs):
    """Download the latest official list of `EQSL.cc`__ users. The list of users can be found here_.

        Args:
            url (str, optional): Download URL

        Returns:
            list: List containing the callsigns of EQSL users (unicode)

        Raises:
            IOError: When network is unavailable, file can't be downloaded or processed

        Example:
           The following example downloads the EQSL user list and checks if DH1TW is a user:

           >>> from pyhamtools.qsl import get_eqsl_users
           >>> mylist = get_eqsl_users()
           >>> try:
           >>>    mylist.index('DH1TW')
           >>> except ValueError as e:
           >>>    print e
           'DH1TW' is not in list

    .. _here: http://www.eqsl.cc/QSLCard/DownloadedFiles/AGMemberlist.txt

    """

    url = ""

    eqsl = []

    try:
        url = kwargs['url']
    except KeyError:
        url = "http://www.eqsl.cc/QSLCard/DownloadedFiles/AGMemberlist.txt"

    try:
        result = requests.get(url)
    except (ConnectionError, HTTPError, Timeout) as e:
        raise IOError(e)

    if result.status_code == requests.codes.ok:
        eqsl = re.sub("^List.+UTC", "", result.text)
        eqsl = eqsl.upper().split()
    else:
        raise IOError("HTTP Error: " + str(result.status_code))

    return eqsl