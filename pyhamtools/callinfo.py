


class Callinfo(object):
    """
    This is going to going to return information for a callsign
    """

    def __init__(self, lookuplib):
        pass

    def getHomeCall(self, callsign):
        """verify call and strip off any /ea1 vp5/ /qrp etc"""
        raise NotImplementedError

    def isValidCall(self, callsign):
        raise NotImplementedError

    def get_prefix(self, callsign):
        raise NotImplementedError

    def getLatLong(self, callsign):
        raise NotImplementedError

    def getCQZone(self, callsign):
        raise NotImplementedError

    def getITUZone(self, prefix):
        raise NotImplementedError

    def getCountry(self, prefix):
        raise NotImplementedError

    def getAdifID(self, prefix):
        raise NotImplementedError

    def getContinent(self, prefix):
        raise NotImplementedError

    def getAll(self, callsign):
        raise NotImplementedError
