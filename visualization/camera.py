import math


class Camera:
    def __init__(self, angle_of_rotation_x, angle_of_rotation_y,
                 angle_of_rotation_z):
        self.rotation = False
        self.angle_of_rotation_x = angle_of_rotation_x
        self.angle_of_rotation_y = angle_of_rotation_y
        self.angle_of_rotation_z = angle_of_rotation_z

    @property
    def angle_of_rotation_x(self):
        return self._angle_of_rotation_x

    @angle_of_rotation_x.setter
    def angle_of_rotation_x(self, angle_of_rotation_x):
        self._angle_of_rotation_x = angle_of_rotation_x
        radians = math.radians(self._angle_of_rotation_x)
        self.cos_a_x = math.cos(radians)
        self.sin_a_x = math.sin(radians)

    @property
    def angle_of_rotation_y(self):
        return self._angle_of_rotation_y

    @angle_of_rotation_y.setter
    def angle_of_rotation_y(self, angle_of_rotation_y):
        self._angle_of_rotation_y = angle_of_rotation_y
        radians = math.radians(self._angle_of_rotation_y)
        self.cos_a_y = math.cos(radians)
        self.sin_a_y = math.sin(radians)

    @property
    def angle_of_rotation_z(self):
        return self._angle_of_rotation_z

    @angle_of_rotation_z.setter
    def angle_of_rotation_z(self, angle_of_rotation_z):
        self._angle_of_rotation_z = angle_of_rotation_z
        radians = math.radians(self._angle_of_rotation_z)
        self.cos_a_z = math.cos(radians)
        self.sin_a_z = math.sin(radians)

    def rotate_x(self, point3d):
        y = point3d.y*self.cos_a_x - point3d.z*self.sin_a_x
        z = point3d.y*self.sin_a_x + point3d.z*self.cos_a_x
        return point3d.x, y, z

    def rotate_y(self, point3d):
        x = point3d.x*self.cos_a_y + point3d.z*self.sin_a_y
        z = point3d.x*(-self.sin_a_y) + point3d.z*self.cos_a_y
        return x, point3d.y, z

    def rotate_z(self, point3d):
        x = point3d.x*self.cos_a_z - point3d.y*self.sin_a_z
        y = point3d.x*self.sin_a_z + point3d.y*self.cos_a_z
        return x, y, point3d.z
