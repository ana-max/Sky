import unittest
from astronomical_calculations.sky_coordinate_systems\
    import Equatorial, Horizontal, Cartesian
from visualization.observer import Observer
from stars_parser import Parser
from collections import namedtuple
Date = namedtuple('Date', 'day month year hour minute second')
Time = namedtuple('Time', 'hour minute second')


class EquatorialTest(unittest.TestCase):
    def setUp(self):
        self.converter = Equatorial('18:32:21', '+23:13:10')
        self.converter2 = Equatorial('18:32', '+23:13')
        # наблюдатель в нулевом меридиане
        self.observer = Observer('00:00:00',
                                 '00:00:00', '60:00:00', '(0,0,0)', '21:56:30')

    def test_gmt_to_gst(self):
        gmt = Date(22, 4, 1980, 14, 36, 51.67)
        gst = self.converter.gmt_to_gst(gmt)
        self.assertEqual(gst, Time(4.0, 40.0, 5.163600000000201))

    def test_get_const_b(self):
        b = self.converter.get_const_b(1979)
        self.assertEqual(b, 17.395559)

    def test_gst_to_lst(self):
        gst = Time(4.0, 40.0, 5.17)
        observer = Observer('-64:00:00',
                            '00:00:00', '60:00:00', '(0,0,0)', '21:30:50')
        lst = self.converter.gst_to_lst(gst, observer)
        self.assertEqual(lst, Time(0.0, 24.0, 5.1699999999991775))

    def test_find_julian_date_month_more_two(self):
        jd = self.converter.find_julian_date(Date(12, 8, 2018, 0, 0, 0))
        self.assertEqual(jd, 2458342.5)

    def test_find_julian_date_month_less_two(self):
        jd = self.converter.find_julian_date(Date(12, 1, 2018, 0, 0, 0))
        self.assertEqual(jd, 2458130.5)

    def test_equatorial_to_horizontal(self):
        horizontal = self.converter.equatorial_to_horizontal(self.observer)
        self.assertEqual(horizontal.azimuth, 293.730630480783)
        self.assertEqual(horizontal.h, 11.574299229619768)

    def test_equatorial_to_horizontal_double(self):
        horizontal = self.converter2.equatorial_to_horizontal(self.observer)
        self.assertEqual(horizontal.azimuth, 293.72062154184573)
        self.assertEqual(horizontal.h, 11.494437665219495)


class HorizontalTest(unittest.TestCase):
    def setUp(self):
        self.converter = Horizontal(90, 60)

    def test_right_zd(self):
        zd = self.converter.zd
        self.assertEqual(zd, 30.0)

    def test_right_cartesian_coordinates(self):
        cartesian = self.converter.horizontal_to_cartesian()
        self.assertEqual(cartesian.x, 3.0616169978683824e-17)
        self.assertEqual(cartesian.y, 0.49999999999999994)
        self.assertEqual(cartesian.z, 0.8660254037844387)


class CartesianTest(unittest.TestCase):
    def setUp(self):
        self.converter = Cartesian(1, 2, 3)
        self.observer = Observer('-64:00:00',
                                 '00:00:00', '60:00:00', '(0,0,0)', '21:30:50')

    def test_convert_to_screen(self):
        screen = self.converter.cartesian_to_screen(self.observer)
        self.assertEqual(screen.x, 0.5773502691896258)
        self.assertEqual(screen.y, 1.1547005383792517)

    def test_to_string(self):
        screen = Cartesian(1, 1, 1).cartesian_to_screen(self.observer)
        self.assertEqual(str(screen),
                         '(1.7320508075688776,1.7320508075688776)')


if __name__ == '__main__':
    unittest.main()
