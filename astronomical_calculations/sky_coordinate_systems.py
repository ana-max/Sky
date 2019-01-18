from astronomical_calculations.angle_converter import AngleConverter
import calendar
import math
from collections import namedtuple
from functools import lru_cache
Date = namedtuple('Date', 'day month year hour minute second')
Time = namedtuple('Time', 'hour minute second')


class Equatorial(AngleConverter):
    def __init__(self, ra, decline):
        self.ra = ra
        self.decline = decline

    @staticmethod
    def find_julian_date(date):
        year1 = date.year - 1 if date.month <= 2 else date.year
        month1 = date.month + 12 if date.month <= 2 else date.month
        support_const_a = year1 // 100
        support_const_b = 2 - support_const_a + support_const_a // 4
        support_const_c = math.modf(365.25 * year1)[1]
        support_const_d = math.modf(30.6001 * (month1 + 1))[1]
        return support_const_b + support_const_c \
            + support_const_d + date.day + 1720994.5

    @lru_cache(maxsize=256)
    def gst_to_lst(self, gst, observer):
        """Convert Greenwich Several Time to Local Sidereal Time"""
        gst = self.time_to_hours_and_piece_of_hour(gst)
        longitude = observer.longitude / 15
        lst = gst + longitude if \
            observer.is_eastern_longitude else gst - longitude
        lst = lst - 24 if lst > 24 else lst + 24 if lst < 0 else lst
        return self.hours_and_piece_of_hour_to_time(lst)

    @lru_cache(maxsize=256)
    def equatorial_to_horizontal(self, observer):
        """This function convert equatorial coordinates to horizontal"""
        st = self.right_ascension_to_time_angle(observer)
        st = self.time_to_hours_and_piece_of_hour(st)
        st *= 15
        decline = self.conversion_to_degrees(self.decline)
        decline = math.radians(decline)
        latitude, st = map(math.radians, [observer.latitude, st])
        sinzd = math.sin(decline)*math.sin(latitude) \
            + math.cos(decline)*math.cos(latitude)*math.cos(st)
        h = math.degrees(math.asin(sinzd))
        coszd = math.sqrt(1 - sinzd**2)
        cosaz = (math.sin(decline) - math.sin(latitude)*sinzd)\
            / (math.cos(latitude)*coszd)
        sinst = math.sin(st)
        az = 360 - math.degrees(math.acos(cosaz)) \
            if sinst > 0 else math.degrees(math.acos(cosaz))
        return Horizontal(az, h)

    @lru_cache(maxsize=256)
    def right_ascension_to_time_angle(self, observer):
        greenwich_several_time = self.gmt_to_gst(observer.greenwich_mean_time)
        local_several_time = self.gst_to_lst(greenwich_several_time, observer)
        right_ascension = self.ra.split(':')
        if len(right_ascension) == 2:
            right_ascension.append('00')
        right_ascension = self.\
            time_to_hours_and_piece_of_hour(Time(*right_ascension))
        local_several_time = self.\
            time_to_hours_and_piece_of_hour(local_several_time)
        time_angle = local_several_time - right_ascension
        time_angle = time_angle - 24 if time_angle > 24 \
            else time_angle + 24 if time_angle < 0 else time_angle
        return self.hours_and_piece_of_hour_to_time(time_angle)

    def gmt_to_gst(self, greenwich_mean_time):
        """Convert Greenwich Mean Time To Greenwich Several Time"""
        month = greenwich_mean_time.month
        day = greenwich_mean_time.day
        year = greenwich_mean_time.year
        count_of_days = 0
        for i in range(1, month):
            count_of_days += calendar.monthrange(year, i)[1]
        count_of_days += day
        count_of_days *= 0.0657098
        const_b = self.get_const_b(year)
        t0 = count_of_days - const_b
        gmt = self.time_to_hours_and_piece_of_hour(greenwich_mean_time)
        gmt *= 1.002738
        gst = gmt + t0
        gst = round(gst - 24 if gst > 24 else gst + 24 if gst < 0 else gst, 6)
        return self.hours_and_piece_of_hour_to_time(gst)

    @lru_cache(maxsize=256)
    def get_const_b(self, year):
        """"This function find const B which is changing every year"""
        date = Date(0, 1, year, 0, 0, 0)
        jd = self.find_julian_date(date)
        s = jd - 2415020.0
        t = s/36525.0
        r = 6.6460656 + 2400.051262*t + 0.00002581*t**2
        u = r - 24*(year - 1900)
        return round(24 - u, 6)


class Horizontal(AngleConverter):
    def __init__(self, azimuth, h):
        zd = math.degrees(math.pi/2) - h
        self.azimuth, self.h, self.zd = azimuth, h, zd

    @lru_cache(maxsize=256)
    def horizontal_to_cartesian(self):
        """This function convert horizontal coordinates to cartesian"""
        azimuth, zd = map(math.radians, [self.azimuth, self.zd])
        x = math.sin(zd)*math.cos(azimuth)
        y = math.sin(zd)*math.sin(azimuth)
        z = math.cos(zd)
        return Cartesian(x, y, z)


class Cartesian:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def get_homogeneous_coordinates(self, w):
        if w == 0:
            raise ValueError('parameter w should be positive')
        self.x *= w
        self.y *= w
        self.z *= w
        self.w = w
        return self

    def cartesian_to_screen(self, observer):
        vector = self.get_homogeneous_coordinates(1)
        fov = math.radians(observer.angle)
        yscale = math.cos(fov/2)/math.sin(fov/2)
        xscale = yscale
        near_zone = 0
        far_zone = 2
        a = far_zone/(far_zone-near_zone)
        b = -(near_zone*far_zone)/(far_zone-near_zone)
        distance = 1
        x = (distance*vector.x*xscale)
        y = vector.y*yscale
        z = vector.z*a+vector.w*b
        w = 1
        x = distance*x/(w*z)
        y = distance*y/(w*z)
        return Screen(x, y)


class Screen:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '({},{})'.format(self.x, self.y)
