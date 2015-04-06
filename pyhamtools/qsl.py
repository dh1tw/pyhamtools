from datetime import datetime
import re

import requests
import redis
from requests.exceptions import ConnectionError, HTTPError, Timeout

def get_lotw_users(**kwargs):
    """Download the latest inoffical list of `ARRL Logbook of the World (LOTW)`__ users which is provided on a weekly basis by HB9BZA_. Dates of the users last upload is added by WD5EAE_.  

        Args:
            url (str, optional): Download URL

        Returns:
            dict: Dictionary containing the callsign (unicode) date of estimated last LOTW upload (datetime)

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
    .. _HB9BZA: http://www.hb9bza.net/lotw-users-list
    .. _WD5EAE: http://www.wd5eae.org/HB9BZA_LoTWUsersList.html
    __ ARRL_ 

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

def get_eqsl_users(**kwargs):
    """Download the latest official list of EQSL.cc users. The list of users can be found here_.

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