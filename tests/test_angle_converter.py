import unittest
from astronomical_calculations.angle_converter import AngleConverter


class AngleConverterTest(unittest.TestCase):
    def setUp(self):
        self.converter = AngleConverter()

    def test_time_to_degree_time(self):
        degree_time = self.converter.time_to_degree_time('21:35:00'.split(':'))
        self.assertEqual(degree_time, ['315.0', '525.0', '0.0'])

    def test_time_conversion_to_degree(self):
        time = self.converter.time_conversion_to_degrees('21:35')
        self.assertEqual(time, 323.75)


if __name__ == '__main__':
    unittest.main()
