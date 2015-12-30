from __future__ import division
from math import pi, sin, cos, atan2, sqrt, radians, log, tan, degrees
from datetime import datetime

import pytz
import ephem

UTC = pytz.UTC

def latlong_to_locator (latitude, longitude):
    """converts WGS84 coordinates into the corresponding Maidenhead Locator

        Args:
            latitude (float): Latitude
            longitude (float): Longitude

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

    if longitude >= 180 or longitude <= -180:
        raise ValueError

    if latitude >= 90 or latitude <= -90:
        raise ValueError

    longitude += 180;
    latitude +=90;

    locator = chr(ord('A') + int(longitude / 20))
    locator += chr(ord('A') + int(latitude / 10))
    locator += chr(ord('0') + int((longitude % 20) / 2))
    locator += chr(ord('0') + int(latitude % 10))
    locator += chr(ord('A') + int((longitude - int(longitude / 2) * 2) / (2 / 24)))
    locator += chr(ord('A') + int((latitude - int(latitude / 1) * 1 ) / (1 / 24)))

    return locator

def locator_to_latlong (locator):
    """converts Maidenhead locator in the corresponding WGS84 coordinates

        Args:
            locator (string): Locator, either 4 or 6 characters

        Returns:
            tuple (float, float): Latitude, Longitude

        Raises:
            ValueError: When called with wrong or invalid input arg
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

    if len(locator) == 5 or len(locator) < 4:
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

    longitude = (ord(locator[0]) - ord('A')) * 20 - 180
    latitude = (ord(locator[1]) - ord('A')) * 10 - 90
    longitude += (ord(locator[2]) - ord('0')) * 2
    latitude += (ord(locator[3]) - ord('0'))

    if len(locator) == 6:
        longitude += ((ord(locator[4])) - ord('A')) * (2 / 24)
        latitude += ((ord(locator[5])) - ord('A')) * (1 / 24)

        # move to center of subsquare
        longitude += 1 / 24
        latitude += 0.5 / 24

    else:
        # move to center of square
        longitude += 1;
        latitude += 0.5;

    return latitude, longitude


def calculate_distance(locator1, locator2):
    """calculates the (shortpath) distance between two Maidenhead locators

        Args:
            locator1 (string): Locator, either 4 or 6 characters
            locator2 (string): Locator, either 4 or 6 characters

        Returns:
            float: Distance in km

        Raises:
            ValueError: When called with wrong or invalid input arg
            AttributeError: When args are not a string

        Example:
           The following calculates the distance between two Maidenhead locators in km

           >>> from pyhamtools.locator import calculate_distance
           >>> calculate_distance("JN48QM", "QF67bf")
           16466.413

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

    return d;


def calculate_distance_longpath(locator1, locator2):
    """calculates the (longpath) distance between two Maidenhead locators

        Args:
            locator1 (string): Locator, either 4 or 6 characters
            locator2 (string): Locator, either 4 or 6 characters

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

    """

    c = 40008 #[km] earth circumference
    sp = calculate_distance(locator1, locator2)

    return c - sp


def calculate_heading(locator1, locator2):
    """calculates the heading from the first to the second locator

        Args:
            locator1 (string): Locator, either 4 or 6 characters
            locator2 (string): Locator, either 4 or 6 characters

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
            locator1 (string): Locator, either 4 or 6 characters
            locator2 (string): Locator, either 4 or 6 characters

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

    """

    heading = calculate_heading(locator1, locator2)

    lp = (heading + 180)%360

    return lp

def calculate_sunrise_sunset(locator, calc_date=datetime.utcnow()):
    """calculates the next sunset and sunrise for a Maidenhead locator at a give date & time

        Args:
            locator1 (string): Maidenhead Locator, either 4 or 6 characters
            calc_date (datetime, optional): Starting datetime for the calculations (UTC)

        Returns:
            dict: Containing datetimes for morning_dawn, sunrise, evening_dawn, sunset

        Raises:
            ValueError: When called with wrong or invalid input arg
            AttributeError: When args are not a string

        Example:
           The following calculates the next sunrise & sunset for JN48QM on the 1./Jan/2014

           >>> from pyhamtools.locator import calculate_sunrise_sunset
           >>> from datetime import datetime
           >>> import pytz
           >>> UTC = pytz.UTC
           >>> myDate = datetime(year=2014, month=1, day=1, tzinfo=UTC)
           >>> calculate_sunrise_sunset("JN48QM", myDate)
           {
               'morning_dawn': datetime.datetime(2014, 1, 1, 6, 36, 51, 710524, tzinfo=<UTC>),
               'sunset': datetime.datetime(2014, 1, 1, 16, 15, 23, 31016, tzinfo=<UTC>),
               'evening_dawn': datetime.datetime(2014, 1, 1, 15, 38, 8, 355315, tzinfo=<UTC>),
               'sunrise': datetime.datetime(2014, 1, 1, 7, 14, 6, 162063, tzinfo=<UTC>)
           }

    """
    morning_dawn = None
    sunrise = None
    evening_dawn = None
    sunset = None

    latitude, longitude = locator_to_latlong(locator)

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
        result['morning_dawn'] = morning_dawn.replace(tzinfo=UTC)
    if sunrise:
        result['sunrise'] = sunrise.replace(tzinfo=UTC)
    if evening_dawn:
        result['evening_dawn'] = evening_dawn.replace(tzinfo=UTC)
    if sunset:
        result['sunset'] = sunset.replace(tzinfo=UTC)
    return result
