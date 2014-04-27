import re
import logging
from datetime import datetime


import pytz


from pyhamtools import LookupLib
from pyhamtools.consts import LookupConventions as const


UTC = pytz.UTC
timestamp_now = datetime.utcnow().replace(tzinfo=UTC)


class Callinfo(object):
    """
    This is going to going to return information for a callsign
    """

    def __init__(self, lookuplib=LookupLib(), logger=None):

        self._logger = None
        if logger:
            self._logger = logger
        else:
            self._logger = logging.getLogger(__name__)
            self._logger.addHandler(logging.NullHandler())

        self._lookuplib = lookuplib
        self._callsign_info = None

    def get_homecall(self, callsign):
        """verify call and strip off any /ea1 vp5/ /qrp etc"""

        callsign = callsign.upper()
        homecall = re.search('[\d]{0,1}[A-Z]{1,2}\d([A-Z]{1,4}|\d{3,3}|\d{1,3}[A-Z])[A-Z]{0,5}', callsign)
        if homecall:
            homecall = homecall.group(0)
            return homecall
        else:
            return

    def _iterate_prefix(self, callsign, timestamp=timestamp_now):
        """truncate call until it corresponds to a Prefix in the database"""
        prefix = callsign

        while(len(prefix) > 0):
            try:
                return self._lookuplib.lookup_prefix(prefix, timestamp)
            except KeyError:
                prefix = prefix.replace(' ', '')[:-1]
                continue
        raise KeyError

    def _dismantle_callsign(self, callsign, timestamp=timestamp_now):

        entire_callsign = callsign.upper()

        if re.search('[/A-Z0-9\-]{3,15}', entire_callsign):  # make sure the call has at least 3 characters

            if re.search('\-\d{1,3}$', entire_callsign):  # cut off any -10 / -02 appendixes
                callsign = re.sub('\-\d{1,3}$', '', entire_callsign)

            if re.search('/[A-Z0-9]{2,4}/[A-Z0-9]{1,4}$', callsign):
                callsign = re.sub('/[A-Z0-9]{1,4}$', '', callsign)  # cut off 2. appendix DH1TW/HC2/P -> DH1TW/HC2

            # multiple character appendix (callsign/xxx)
            if re.search('/[A-Z0-9]{2,4}$', callsign):  # case call/xxx, but ignoring /p and /m or /5
                appendix = re.search('/[A-Z0-9]{2,4}$', callsign)
                appendix = re.sub('/', '', appendix.group(0))
                self._logger.debug("appendix: " + appendix)

                if appendix == 'MM':  # special case Martime Mobile
                    #self._mm = True
                    raise KeyError
                elif appendix == 'AM':  # special case Aeronautic Mobile
                    #self._am = True
                    raise KeyError
                elif appendix == 'QRP':  # special case QRP
                    callsign = re.sub('/QRP', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)
                elif appendix == 'QRPP':  # special case QRPP
                    callsign = re.sub('/QRPP', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)
                elif appendix == 'BCN':  #filter all beacons
                    callsign = re.sub('/BCN', '', callsign)
#                    self.beacon = True
                    return self._iterate_prefix(callsign, timestamp)
                elif appendix == "LH":  #Filter all Lighthouses
                    callsign = re.sub('/LH', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)
                else:
                    #check if the appendix is a valid country prefix
                    return self._iterate_prefix(re.sub('/', '', appendix), timestamp)

            # Single character appendix (callsign/x)
            elif re.search('/[A-Z0-9]$', callsign):  # case call/p or /b /m or /5 etc.
                appendix = re.search('/[A-Z0-9]$', callsign)
                appendix = re.sub('/', '', appendix.group(0))

                if appendix == 'B':  #special case Beacon
                    callsign = re.sub('/B', '', callsign)
                    return self._iterate_prefix(callsign, timestamp)
                    # self.beacon = True

                elif re.search('\d$', appendix):
                    area_nr = re.search('\d$', appendix).group(0)
                    callsign = re.sub('/\d$', '', callsign)
                    callsign = re.sub('[\d]+', area_nr, callsign)
                    return self._iterate_prefix(callsign, timestamp)

                else:
                    return self._iterate_prefix(callsign, timestamp)

            # regular callsigns, without prefix or appendix
            elif re.match('^[\d]{0,1}[A-Z]{1,2}\d([A-Z]{1,4}|\d{3,3}|\d{1,3}[A-Z])[A-Z]{0,5}$', callsign):
                return self._iterate_prefix(callsign, timestamp)

            # callsigns with prefixes (xxx/callsign)
            elif re.search('^[A-Z0-9]{1,4}/', entire_callsign):
                pfx = re.search('^[A-Z0-9]{1,4}/', entire_callsign)
                pfx = re.sub('/', '', pfx.group(0))
                return self._iterate_prefix(pfx)

        self._logger.debug("Could not decode " + callsign)
        raise KeyError

    def _lookup_callsign(self, callsign, timestamp=timestamp_now):

        # Check if operation is invalid
        invalid = False
        try:
            if self._lookuplib.is_invalid_operation(callsign, timestamp):
                invalid = True
                raise KeyError
        except KeyError:
            if invalid:
                raise

        # Check if a dedicated entry exists for the callsign
        try:
            return self._lookuplib.lookup_callsign(callsign, timestamp)
        except KeyError:
            pass

        # Dismantel the callsign and check if the prefix is known
        return self._dismantle_callsign(callsign, timestamp)


    def get_all(self, callsign, timestamp=timestamp_now):

        callsign_data = self._lookup_callsign(callsign, timestamp_now)

        try:
            cqz = self._lookuplib.lookup_zone_exception(callsign, timestamp)
            callsign_data[const.CQZ] = cqz
        except KeyError:
            pass

        print callsign_data

        return callsign_data

    def is_valid_callsign(self, callsign, timestamp=timestamp_now):
        try:
            if self.get_all(callsign, timestamp):
                return True
        except:
            return False

    def get_lat_long(self, callsign):
        callsign_data = self.get_all(callsign, timestamp=timestamp_now)
        return {
            const.LATITUDE : callsign_data[const.LATITUDE],
            const.LONGITUDE : callsign_data[const.LONGITUDE]
        }

    def get_cqz(self, callsign, timestamp=timestamp_now):
        return self.get_all(callsign, timestamp)[const.CQZ]

    def get_ituz(self, callsign, timestamp=timestamp_now):
        return self.get_all(callsign, timestamp)[const.ITUZ]

    def get_country_name(self, callsign, timestamp=timestamp_now):
        return self.get_all(callsign, timestamp)[const.COUNTRY]

    def get_adif_id(self, callsign, timestamp=timestamp_now):
        return self.get_all(callsign, timestamp)[const.ADIF]

    def get_continent(self, callsign, timestamp=timestamp_now):
        return self.get_all(callsign, timestamp)[const.CONTINENT]

if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig("logging.ini")
    logger = logging.getLogger(__name__)


    from pyhamtools import LookupLib
    apikey = "67547d6ce7a37276373b0568e3e52c1d3e2cb0e5"
    l = LookupLib("clublogxml", apikey=apikey)
    c = Callinfo(l)
    print c._iterate_prefix("DH1TW")
    print c._iterate_prefix("QRM")

