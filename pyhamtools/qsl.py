from datetime import datetime
import re

import requests
import redis
from requests.exceptions import ConnectionError, HTTPError, Timeout


def get_lotw_users(**kwargs):
    """download the latest list of ARRL Logbook of the World (LOTW) inofficial user list
       which is provided on a weekly basis by `HB9BZA`_. Dates of last activity on LOTW
       is added by `WD5EAE`_.  

        Args:
            url (str, optional): Download URL

        Returns:
            dict: Dictionary containing the callsign (unicode) date of estimated last LOTW upload (datetime)

        Raises:
            IOError: When network is unavailable, file can't be downloaded or processed

        Example:
           The following example downloads the LOTW user list and check when DH1TW has made his last LOTW upload:

           >>> from pyhamtools.qsl import get_lotw_users
           >>> mydict = get_lotw_users()
           >>> mydict['DH1TW']
           datetime.datetime(2014, 9, 7, 0, 0)
                
    .. HB9BZA: http://www.hb9bza.net/lotw-users-list
    .. WD5EAE: http://www.wd5eae.org/HB9BZA_LoTWUsersList.html

    """    
    url = ""
    
    lotw = {}
    
    try: 
        url = kwargs['url']
    except KeyError:
        # url = "http://wd5eae.org/LoTW1.txt"
        url = "http://wd5eae.org/LoTW_Data.txt"
    
    try: 
        result = requests.get(url)
    except (ConnectionError, HTTPError, Timeout) as e:
        raise IOError(e)

    if result.status_code == requests.codes.ok:
        for el in result.text.split():
            data = el.split(",")
            lotw[data[0]] = datetime.strptime(data[1], '%Y-%m-%d')
        #     print call
    else: 
        raise IOError("HTTP Error: " + str(result.status_code))
        
    return lotw

def get_eqsl_users(**kwargs):
    """download the latest official list of EQSL.cc users. The list of users can be found `here`_.

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
                
    .. here: http://www.eqsl.cc/QSLCard/DownloadedFiles/AGMemberlist.txt
    .. WD5EAE: http://www.wd5eae.org/HB9BZA_LoTWUsersList.html

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