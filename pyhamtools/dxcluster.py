__author__ = 'dh1tw'

from datetime import datetime
from time import strptime, mktime
import re

import pytz

from pyhamtools.consts import LookupConventions as const


UTC = pytz.UTC



def decode_char_spot(raw_string):
    """Chop Line from DX-Cluster into pieces and return a dict with the spot data"""

    data = {}

    # Spotter callsign
    if re.match('[A-Za-z0-9\/]+[:$]', raw_string[6:15]):
        data[const.SPOTTER] = re.sub(':', '', re.match('[A-Za-z0-9\/]+[:$]', raw_string[6:15]).group(0))
    else:
        raise ValueError

    if re.search('[0-9\.]{5,12}', raw_string[10:25]):
        data[const.FREQUENCY] = float(re.search('[0-9\.]{5,12}', raw_string[10:25]).group(0))
    else:
        raise ValueError

    data[const.DX] = re.sub('[^A-Za-z0-9\/]+', '', raw_string[26:38])
    data[const.COMMENT] = re.sub('[^\sA-Za-z0-9\.,;\#\+\-!\?\$\(\)@\/]+', ' ', raw_string[39:69]).strip()
    data[const.TIME] = datetime.now().replace(tzinfo=UTC)

    return data

def decode_pc11_message(raw_string):
    """Decode PC11 message, which usually contains DX Spots"""

    data = {}
    spot = raw_string.split("^")
    data[const.FREQUENCY] = float(spot[1])
    data[const.DX] = spot[2]
    data[const.TIME] = datetime.fromtimestamp(mktime(strptime(spot[3]+" "+spot[4][:-1], "%d-%b-%Y %H%M")))
    data[const.COMMENT] = spot[5]
    data[const.SPOTTER] = spot[6]
    data["node"] = spot[7]
    data["raw_spot"] = raw_string
    return data


def decode_pc61_message(raw_string):
    """Decode PC61 message, which usually contains DX Spots"""

    data = {}
    spot = raw_string.split("^")
    data[const.FREQUENCY] = float(spot[1])
    data[const.DX] = spot[2]
    data[const.TIME] = datetime.fromtimestamp(mktime(strptime(spot[3]+" "+spot[4][:-1], "%d-%b-%Y %H%M")))
    data[const.COMMENT] = spot[5]
    data[const.SPOTTER] = spot[6]
    data["node"] = spot[7]
    data["ip"] = spot[8]
    data["raw_spot"] = raw_string
    return data

def decode_pc23_message(raw_string):
    """ Decode PC23 Message which usually contains WCY """

    data = {}
    wcy = raw_string.split("^")
    data[const.R] = int(wcy[1])
    data[const.expk] = int(wcy[2])
    data[const.CALLSIGN] = wcy[3]
    data[const.A] = wcy[4]
    data[const.SFI] = wcy[5]
    data[const.K] = wcy[6]
    data[const.AURORA] = wcy[7]
    data["node"] = wcy[7]
    data["ip"] = wcy[8]
    data["raw_data"] = raw_string
    return data

