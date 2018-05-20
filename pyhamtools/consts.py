

class LookupConventions:
    """ This class defines the constants used within the pyhamtools package """

    # Mostly specific to Clublog XML File
    CALLSIGN = u"callsign"
    COUNTRY = u"country"
    PREFIX = u"prefix"
    ADIF = u"adif"
    CQZ = u"cqz"
    ITUZ = u"ituz"
    CONTINENT = u"continent"
    LATITUDE = u"latitude"
    LONGITUDE = u"longitude"
    START = u"start"
    END = u"end"
    WHITELIST = u"whitelist"
    WHITELIST_START = u"whitelist_start"
    WHITELIST_END = u"whitelist_end"
    DELETED = u"deleted"
    MARITIME_MOBILE = u"mm"
    AIRCRAFT_MOBILE = u"am"
    LOCATOR = u"locator"
    BEACON = u"beacon"

    #CQ / DIGITAL Skimmer specific

    SKIMMER = u"skimmer"
    FS = u"fs" #fieldstrength
    WPM = u"wpm" #words / bytes per second
    CQ = u"cq"
    NCDXF = u"ncdxf"


    # Modes
    CW = u"CW"
    USB = u"USB"
    LSB = u"LSB"
    DIGITAL = u"DIGITAL"
    FM = u"FM"
    FT8 = u'FT8'

    #DX Spot
    SPOTTER = u"spotter"
    DX = u"dx"
    FREQUENCY = u"frequency"
    COMMENT = u"comment"
    TIME = u"time"
    BAND = u"band"
    MODE = u"mode"

    #DX Spider specific
    ORIGIN_NODE = u"node"
    HOPS = u"hops"
    RAW_SPOT = u"raw"
    IP = u"ip"
    ROUTE = u"route"
    TEXT = u"text"
    SYSOP_FLAG = u"sysop_flag"
    WX_FLAG = u"wx_flag"

    #WWV & WCY
    STATION = u"station"
    R = u"r"
    K = u"k"
    EXPK = u"expk"
    SFI = u"sfi"
    A = u"a"
    AURORA = u"aurora"
    SA = u"sa"
    GMF = u"gmf"
    FORECAST = u"forecast"

    #QRZ.com
    XREF = u"xref"
    ALIASES = u"aliases"
    FNAME = u"fname"
    NAME = u"name"
    ADDR1 = u"addr1"
    ADDR2 = u"addr2"
    STATE = u"state"
    ZIPCODE = u"zipcode"
    CCODE = u"ccode"
    COUNTY = u"county"
    FIPS = u"fips"
    LAND = u"land"
    EFDATE = u"efdate"
    EXPDATE = u"expdate"
    P_CALL = u"p_call"
    LICENSE_CLASS = u"license_class"
    CODES = u"codes"
    QSLMGR = u"qslmgr"
    EMAIL = u"email"
    URL = u"url"
    U_VIEWS = u"u_views"
    BIO = u"bio"
    BIODATE = u"biodate"
    IMAGE = u"image"
    IMAGE_INFO = u"imageinfo"
    SERIAL = u"serial"
    MODDATE = u"moddate"
    MSA = "msa"
    AREACODE = "areacode"
    TIMEZONE = "timezone"
    GMTOFFSET = "gmtoffset"
    DST = "dst"
    EQSL = "eqsl"
    MQSL = "mqsl"
    LOTW = "lotw"
    BORN = "born"
    USER_MGR = "user"
    IOTA = "iota"
    GEOLOC = "geoloc"
