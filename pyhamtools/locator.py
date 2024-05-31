from math import pi, sin, cos, atan2, sqrt, radians, log, tan, degrees
from datetime import datetime, timezone

import ephem

def latlong_to_locator (latitude, longitude, precision=6):
    """converts WGS84 coordinates into the corresponding Maidenhead Locator

        Args:
            latitude (float): Latitude
            longitude (float): Longitude
            precision (int): 4,6,8 chars (default 6)

        Returns:
            string: Maidenhead locator

        Raises:
            ValueError: When called with wrong or invalid input args
            TypeError: When args are non float values

        Example:
           The following example converts latitude and longitude into the Maidenhead locator

           >>> from pyhamtools.locator import latlong_to_locator
           >>> latitude = 48.5208333
           >>> longitude = 9.375
           >>> latlong_to_locator(latitude, longitude)
           'JN48QM'

        Note:
             Latitude (negative = West, positive = East)
             Longitude (negative = South, positive = North)

    """

    if precision < 4 or precision ==5 or precision == 7 or precision > 8:
        return ValueError

    if longitude >= 180 or longitude <= -180:
        raise ValueError

    if latitude >= 90 or latitude <= -90:
        raise ValueError

    longitude +=180
    latitude +=90

    # copied & adapted from github.com/space-physics/maidenhead
    A = ord('A')
    a = divmod(longitude, 20)
    b = divmod(latitude, 10)
    locator = chr(A + int(a[0])) + chr(A + int(b[0]))
    lon = a[1] / 2.0
    lat = b[1]
    i = 1

    while i < precision/2:
        i += 1
        a = divmod(lon, 1)
        b = divmod(lat, 1)
        if not (i % 2):
            locator += str(int(a[0])) + str(int(b[0]))
            lon = 24 * a[1]
            lat = 24 * b[1]
        else:
            locator += chr(A + int(a[0])) + chr(A + int(b[0]))
            lon = 10 * a[1]
            lat = 10 * b[1]

    return locator

def locator_to_latlong (locator, center=True):
    """converts Maidenhead locator in the corresponding WGS84 coordinates

        Args:
            locator (string): Locator, either 4, 6 or 8 characters
            center (bool): Center of (sub)square. By default True. If False, the south/western corner will be returned

        Returns:
            tuple (float, float): Latitude, Longitude

        Raises:
            ValueError: When called with wrong or invalid Maidenhead locator string
            TypeError: When arg is not a string

        Example:
           The following example converts a Maidenhead locator into Latitude and Longitude

           >>> from pyhamtools.locator import locator_to_latlong
           >>> latitude, longitude = locator_to_latlong("JN48QM")
           >>> print latitude, longitude
           48.5208333333 9.375

        Note:
             Latitude (negative = West, positive = East)
             Longitude (negative = South, positive = North)

    """

    locator = locator.upper()

    if len(locator) < 4 or len(locator) == 5 or len(locator) == 7:
        raise ValueError

    if ord(locator[0]) > ord('R') or ord(locator[0]) < ord('A'):
        raise ValueError

    if ord(locator[1]) > ord('R') or ord(locator[1]) < ord('A'):
        raise ValueError

    if ord(locator[2]) > ord('9') or ord(locator[2]) < ord('0'):
        raise ValueError

    if ord(locator[3]) > ord('9') or ord(locator[3]) < ord('0'):
        raise ValueError

    if len(locator) == 6:
        if ord(locator[4]) > ord('X') or ord(locator[4]) < ord('A'):
            raise ValueError
        if ord (locator[5]) > ord('X') or ord(locator[5]) < ord('A'):
            raise ValueError

    if len(locator) == 8:
        if ord(locator[6]) > ord('9') or ord(locator[6]) < ord('0'):
            raise ValueError
        if ord (locator[7]) > ord('9') or ord(locator[7]) < ord('0'):
            raise ValueError

    longitude = (ord(locator[0]) - ord('A')) * 20 - 180
    latitude = (ord(locator[1]) - ord('A')) * 10 - 90
    longitude += (ord(locator[2]) - ord('0')) * 2
    latitude += (ord(locator[3]) - ord('0')) * 1

    if len(locator) == 4:

        if center:
            longitude += 2 / 2
            latitude += 1.0 / 2

    elif len(locator) == 6:
        longitude += (ord(locator[4]) - ord('A')) * 5.0 / 60
        latitude += (ord(locator[5]) - ord('A')) * 2.5 / 60

        if center:
            longitude += 5.0 / 60 / 2
            latitude += 2.5 / 60 / 2

    elif len(locator) == 8:
        longitude += (ord(locator[4]) - ord('A')) * 5.0 / 60
        latitude += (ord(locator[5]) - ord('A')) * 2.5 / 60

        longitude += int(locator[6]) * 5.0 / 600
        latitude += int(locator[7]) * 2.5 / 600

        if center:
            longitude += 5.0 / 600 / 2
            latitude += 2.5 / 600 / 2

    else:
        raise ValueError

    return latitude, longitude


def calculate_distance(locator1, locator2):
    """calculates the (shortpath) distance between two Maidenhead locators

        Args:
            locator1 (string): Locator, either 4, 6 or 8 characters
            locator2 (string): Locator, either 4, 6 or 8 characters

        Returns:
            float: Distance in km

        Raises:
            ValueError: When called with wrong or invalid maidenhead locator strings
            AttributeError: When args are not a string

        Example:
           The following calculates the distance between two Maidenhead locators in km

           >>> from pyhamtools.locator import calculate_distance
           >>> calculate_distance("JN48QM", "QF67bf")
           16466.413

        Note:
            Distances is calculated between the centers of the (sub) squares

    """

    R = 6371 #earh radius
    lat1, long1 = locator_to_latlong(locator1)
    lat2, long2 = locator_to_latlong(locator2)

    d_lat = radians(lat2) - radians(lat1)
    d_long = radians(long2) - radians(long1)

    r_lat1 = radians(lat1)
    r_long1 = radians(long1)
    r_lat2 = radians(lat2)
    r_long2 = radians(long2)

    a = sin(d_lat/2) * sin(d_lat/2) + cos(r_lat1) * cos(r_lat2) * sin(d_long/2) * sin(d_long/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = R * c #distance in km

    return d


def calculate_distance_longpath(locator1, locator2):
    """calculates the (longpath) distance between two Maidenhead locators

        Args:
            locator1 (string): Locator, either 4, 6 or 8 characters
            locator2 (string): Locator, either 4, 6 or 8 characters

        Returns:
            float: Distance in km

        Raises:
            ValueError: When called with wrong or invalid input arg
            AttributeError: When args are not a string

        Example:
           The following calculates the longpath distance between two Maidenhead locators in km

           >>> from pyhamtools.locator import calculate_distance_longpath
           >>> calculate_distance_longpath("JN48QM", "QF67bf")
           23541.5867

        Note:
            Distance is calculated between the centers of the (sub) squares
    """

    c = 40008 #[km] earth circumference
    sp = calculate_distance(locator1, locator2)

    return c - sp


def calculate_heading(locator1, locator2):
    """calculates the heading from the first to the second locator

        Args:
            locator1 (string): Locator, either 4, 6 or 8 characters
            locator2 (string): Locator, either 4, 6 or 6 characters

        Returns:
            float: Heading in deg

        Raises:
            ValueError: When called with wrong or invalid input arg
            AttributeError: When args are not a string

        Example:
           The following calculates the heading from locator1 to locator2

           >>> from pyhamtools.locator import calculate_heading
           >>> calculate_heading("JN48QM", "QF67bf")
           74.3136

        Note:
            Heading is calculated between the centers of the (sub) squares

    """

    lat1, long1 = locator_to_latlong(locator1)
    lat2, long2 = locator_to_latlong(locator2)

    r_lat1 = radians(lat1)
    r_lon1 = radians(long1)

    r_lat2 = radians(lat2)
    r_lon2 = radians(long2)

    d_lon = radians(long2 - long1)

    b = atan2(sin(d_lon)*cos(r_lat2),cos(r_lat1)*sin(r_lat2)-sin(r_lat1)*cos(r_lat2)*cos(d_lon)) # bearing calc
    bd = degrees(b)
    br,bn = divmod(bd+360,360) # the bearing remainder and final bearing

    return bn

def calculate_heading_longpath(locator1, locator2):
    """calculates the heading from the first to the second locator (long path)

        Args:
            locator1 (string): Locator, either 4, 6 or 8 characters
            locator2 (string): Locator, either 4, 6 or 8 characters

        Returns:
            float: Long path heading in deg

        Raises:
            ValueError: When called with wrong or invalid input arg
            AttributeError: When args are not a string

        Example:
           The following calculates the long path heading from locator1 to locator2

           >>> from pyhamtools.locator import calculate_heading_longpath
           >>> calculate_heading_longpath("JN48QM", "QF67bf")
           254.3136

        Note:
            Distance is calculated between the centers of the (sub) squares

    """

    heading = calculate_heading(locator1, locator2)

    lp = (heading + 180)%360

    return lp

def calculate_sunrise_sunset(locator, calc_date=None):
    """calculates the next sunset and sunrise for a Maidenhead locator at a give date & time

        Args:
            locator1 (string): Maidenhead Locator, either 4, 6 or 8 characters
            calc_date (datetime, optional): Starting datetime for the calculations (UTC)

        Returns:
            dict: Containing datetimes for morning_dawn, sunrise, evening_dawn, sunset

        Raises:
            ValueError: When called with wrong or invalid input arg
            AttributeError: When args are not a string

        Example:
           The following calculates the next sunrise & sunset for JN48QM on the 1./Jan/2014

           >>> from pyhamtools.locator import calculate_sunrise_sunset
           >>> from datetime import datetime, timezone
           >>> myDate = datetime(year=2014, month=1, day=1, tzinfo=timezone.utc)
           >>> calculate_sunrise_sunset("JN48QM", myDate)
           {
               'morning_dawn': datetime.datetime(2014, 1, 1, 6, 36, 51, 710524, tzinfo=datetime.timezone.utc),
               'sunset': datetime.datetime(2014, 1, 1, 16, 15, 23, 31016, tzinfo=datetime.timezone.utc),
               'evening_dawn': datetime.datetime(2014, 1, 1, 15, 38, 8, 355315, tzinfo=datetime.timezone.utc),
               'sunrise': datetime.datetime(2014, 1, 1, 7, 14, 6, 162063, tzinfo=datetime.timezone.utc)
           }

    """
    morning_dawn = None
    sunrise = None
    evening_dawn = None
    sunset = None

    latitude, longitude = locator_to_latlong(locator)

    if calc_date is None:
        calc_date = datetime.now(timezone.utc)
    if type(calc_date) != datetime:
        raise ValueError

    sun = ephem.Sun()
    home = ephem.Observer()

    home.lat = str(latitude)
    home.long = str(longitude)
    home.date = calc_date

    sun.compute(home)

    try:
        nextrise = home.next_rising(sun)
        nextset = home.next_setting(sun)

        home.horizon = '-6'
        beg_twilight = home.next_rising(sun, use_center=True)
        end_twilight = home.next_setting(sun, use_center=True)

        morning_dawn = beg_twilight.datetime()
        sunrise = nextrise.datetime()

        evening_dawn = nextset.datetime()
        sunset = end_twilight.datetime()

    #if sun never sets or rises (e.g. at polar circles)
    except ephem.AlwaysUpError as e:
        morning_dawn = None
        sunrise = None
        evening_dawn = None
        sunset = None
    except ephem.NeverUpError as e:
        morning_dawn = None
        sunrise = None
        evening_dawn = None
        sunset = None

    result = {}
    result['morning_dawn'] = morning_dawn
    result['sunrise'] = sunrise
    result['evening_dawn'] = evening_dawn
    result['sunset'] = sunset

    if morning_dawn:
        result['morning_dawn'] = morning_dawn.replace(tzinfo=timezone.utc)
    if sunrise:
        result['sunrise'] = sunrise.replace(tzinfo=timezone.utc)
    if evening_dawn:
        result['evening_dawn'] = evening_dawn.replace(tzinfo=timezone.utc)
    if sunset:
        result['sunset'] = sunset.replace(tzinfo=timezone.utc)
    return result
