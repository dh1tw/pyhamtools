

class LookupConventions:
    """ This class defines the constants used within the pyhamtools package """

    # Mostly specific to Clublog XML File
    CALLSIGN = "callsign"
    COUNTRY = "country"
    PREFIX = "prefix"
    ADIF = "adif"
    CQZ = "cqz"
    ITUZ = "ituz"
    CONTINENT = "continent"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    START = "start"
    END = "end"
    WHITELIST = "whitelist"
    WHITELIST_START = "whitelist_start"
    WHITELIST_END = "whitelist_end"
    DELETED = "deleted"
    MARITIME_MOBILE = "mm"
    AIRCRAFT_MOBILE = "am"
    BEACON = "beacon"
    SKIMMER = "skimmer"

    # Modes
    CW = "CW"
    USB = "USB"
    LSB = "LSB"
    DIGITAL = "DIGITAL"
    FM = "FM"

    #DX Spot
    SPOTTER = "spotter"
    DX = "dx"
    FREQUENCY = "frequency"
    COMMENT = "comment"
    TIME = "time"
    BAND = "band"
    MODE = "mode"

    #DX Spider specific
    ORIGIN_NODE = "node"
    HOPS = "hops"
    RAW_SPOT = "raw"
    IP = "ip"
    ROUTE = "route"
    TEXT = "text"
    SYSOP_FLAG = "sysop_flag"
    WX_FLAG = "wx_flag"

    #WWV & WCY
    STATION = "station"
    R = "r"
    K = "k"
    EXPK = "expk"
    SFI = "sfi"
    A = "a"
    AURORA = "aurora"
    SA = "sa"
    GMF = "gmf"
    FORECAST = "forecast"
