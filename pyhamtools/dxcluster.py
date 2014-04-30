__author__ = 'dh1tw'

from datetime import datetime
import re


import pytz

UTC = pytz.UTC

from pyhamtools.utils import freq_to_band
from pyhamtools.consts import Modes as mode
from pyhamtools.consts import DXSpot as dxspot


def decode_spot(raw_string):
    """Chop Line from DX-Cluster into pieces and return a dict with the spot data"""

    spotter_call = None
    dx_call = None
    frequency = None
    comment = None
    spot_time = None
    band = None
    mode = None
    bandmode = None

    # Spotter callsign
    if re.match('[A-Za-z0-9\/]+[:$]', raw_string[6:15]):
        spotter_call = re.sub(':', '', re.match('[A-Za-z0-9\/]+[:$]', raw_string[6:15]).group(0))
    else:
        raise ValueError

    if re.search('[0-9\.]{5,12}', raw_string[10:25]):
        frequency = float(re.search('[0-9\.]{5,12}', raw_string[10:25]).group(0))
    else:
        raise ValueError

    dx_call = re.sub('[^A-Za-z0-9\/]+', '', raw_string[26:38])
    comment = re.sub('[^\sA-Za-z0-9\.,;\#\+\-!\?\$\(\)@\/]+', ' ', raw_string[39:69])
    spot_time_ = re.sub('[^0-9]+', '', raw_string[70:74])
    spot_time = datetime(hour=int(spot_time_[0:2]), minute=int(spot_time_[2:4]), second=0, microsecond = 0, tzinfo=UTC)

    try:
        bandmode = freq_to_band(frequency)
        band = bandmode["band"]
        mode = bandmode["mode"]
    except KeyError:
        raise ValueError

    data = {
        dxspot.SPOTTER: spotter_call,
        dxspot.DX: dx_call,
        dxspot.BAND: band,
        dxspot.MODE: mode,
        dxspot.COMMENT: comment,
        dxspot.TIME: spot_time
    }

    return data
