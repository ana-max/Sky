import unittest
from visualization.star import Star


class StarTest(unittest.TestCase):
    def setUp(self):
        self.never_visible_star = Star('19:38.9', '-10:20', '8.0', 'f', 'aql')
        self.visible_star = Star('19:38.9', '-10:20', '6.0', '0M', 'umi')

    def test_is_never_visible(self):
        self.assertTrue(self.never_visible_star.is_never_visible())
        self.assertFalse(self.visible_star.is_never_visible())

    def test_color(self):
        self.assertEqual(self.never_visible_star.color, '#FFFFFF')
        self.assertEqual(self.visible_star.color, '#FF6347')

    def test_radius(self):
        self.assertEqual(self.never_visible_star.radius, None)
        self.assertEqual(self.visible_star.radius, 4)

    def test_parameters(self):
        self.assertEqual(self.visible_star.right_ascension, '19:38.9')
        self.assertEqual(self.visible_star.decline, '-10:20')
        self.assertEqual(self.visible_star.constellation, 'umi')


if __name__ == '__main__':
    unittest.main()
