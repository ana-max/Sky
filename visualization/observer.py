from astronomical_calculations.angle_converter import AngleConverter
from astronomical_calculations.sky_coordinate_systems import Horizontal
from astronomical_calculations.sky_coordinate_systems import Cartesian
from collections import namedtuple
import datetime
from functools import lru_cache
Date = namedtuple('Date', 'day month year hour minute second')


class Observer(AngleConverter):
    def __init__(self, longitude, latitude, angle, vector, time_now):
        self.input_longitude = longitude
        self.input_latitude = latitude
        self.input_angle = angle
        self.input_vector = vector
        vector = vector[1:-1].split(',')
        self.vector = Cartesian(vector[0], vector[1], vector[2])
        longitude = self.conversion_to_degrees(longitude)
        latitude = self.conversion_to_degrees(latitude)
        self.is_eastern_longitude = longitude > 0
        self.is_northern_latitude = latitude > 0
        self.longitude = longitude if longitude > 0 else -longitude
        self.latitude = latitude if latitude > 0 else -latitude
        self.horizontal = Horizontal(self.longitude, self.latitude)
        self.angle = self.conversion_to_degrees(angle)
        self.time_zone = longitude//15
        is_datetime = type(time_now) == datetime.datetime
        if not is_datetime:
            self.input_time_now = time_now
        else:
            self.input_time_now = str(time_now.hour) + ':' + \
                                  str(time_now.minute) + ':' + \
                                  str(time_now.second)
        self.time_now = time_now if is_datetime else \
            self._conversion_to_datetime(time_now)

    @property
    def greenwich_mean_time(self):
        return self._get_greenwich_time()

    @lru_cache(maxsize=256)
    def _get_greenwich_time(self):
        piece_of_hours = self.time_to_hours_and_piece_of_hour(self.time_now)
        greenwich_time = piece_of_hours - self.time_zone
        greenwich_time = greenwich_time - 24 \
            if greenwich_time > 24 else greenwich_time + 24\
            if greenwich_time < 0 else greenwich_time
        time = self.hours_and_piece_of_hour_to_time(greenwich_time)
        return Date(self.time_now.day, self.time_now.month,
                    self.time_now.year, *time)

    def _conversion_to_datetime(self, time):
        date_time = datetime.datetime.now()
        time = time.split(':')
        return Date(date_time.day, date_time.month, date_time.year, *time)
