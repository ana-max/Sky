import unittest
from visualization.camera import Camera
from astronomical_calculations.sky_coordinate_systems import Cartesian


class CameraTest(unittest.TestCase):
    def setUp(self):
        self.camera = Camera(60, 90, 30)

    def test_good_angles(self):
        self.assertEqual(self.camera.angle_of_rotation_x, 60)
        self.assertEqual(self.camera.angle_of_rotation_y, 90)
        self.assertEqual(self.camera.angle_of_rotation_z, 30)

    def test_rotate_x(self):
        point3d = self.camera.rotate_x(Cartesian(30, 30, 30))
        self.assertEqual(point3d[0], 30.0)
        self.assertEqual(point3d[1], -10.980762113533153)
        self.assertEqual(point3d[2], 40.98076211353316)

    def test_rotate_y(self):
        point3d = self.camera.rotate_y(Cartesian(30, 30, 30))
        self.assertEqual(point3d[0], 30.000000000000004)
        self.assertEqual(point3d[1], 30.0)
        self.assertEqual(point3d[2], -29.999999999999996)

    def test_rotate_z(self):
        point3d = self.camera.rotate_z(Cartesian(30, 30, 30))
        self.assertEqual(point3d[0], 10.980762113533162)
        self.assertEqual(point3d[1], 40.98076211353316)
        self.assertEqual(point3d[2], 30.0)


if __name__ == '__main__':
    unittest.main()
