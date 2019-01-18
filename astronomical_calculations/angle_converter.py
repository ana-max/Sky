from math import modf
from collections import namedtuple


class AngleConverter:
    def time_to_degree_time(self, time):
        return [str(float(x) * 15) for x in time]

    def minutes_conversion_to_degrees(self, minutes):
        return float(minutes) / 60

    def seconds_conversion_to_degrees(self, seconds):
        return float(seconds) / 3600

    def time_to_hours_and_piece_of_hour(self, time):
        hours, minutes, seconds = \
            map(float, [time.hour, time.minute, time.second])
        seconds /= 60
        res = (minutes + seconds) / 60
        return res + hours

    def hours_and_piece_of_hour_to_time(self, hours_and_piece_of_hours):
        Time = namedtuple('Time', 'hour minute second')
        dr = modf(hours_and_piece_of_hours)[0] * 60
        minutes = modf(dr)[1]
        seconds = modf(dr)[0]*60
        hours = modf(hours_and_piece_of_hours)[1]
        return Time(hours, minutes, seconds)

    def sign(self, x):
        return 1 if x > 0 else 0 if x == 0 else -1

    def time_conversion_to_degrees(self, time):
        time = time.replace(' ', '').split(':')
        degree_time = self.time_to_degree_time(time)
        return self.conversion_to_degrees(':'.join(degree_time))

    def conversion_to_degrees(self, degrees_minutes_seconds):
        d_m_s = degrees_minutes_seconds.replace(' ', '').split(':')
        if len(d_m_s) == 2:
            d_m_s.append('00')
        degrees = float(d_m_s[0])
        minutes = self.minutes_conversion_to_degrees(d_m_s[1])
        seconds = self.seconds_conversion_to_degrees(d_m_s[2])
        zn = self.sign(degrees)
        return zn*sum([abs(degrees), minutes, seconds])
