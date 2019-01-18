from PyQt5.QtGui import QPainter, QBrush, QPen, QColor, QImage
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QToolTip, QDesktopWidget
from astronomical_calculations import sky_coordinate_systems
from collections import namedtuple
from visualization.camera import Camera
from visualization.observer import Observer
from visualization.data_of_constellations import Data
from visualization.menu import Menu
from stars_parser import Info
import math
Screen = namedtuple('Screen', 'x y radius constellation')
Point2d = namedtuple('Point2d', 'x y color radius constellation')
Side = namedtuple('Side', 'name coordinates color')


class StarsWindow(QMainWindow):
    def __init__(self, data_for_draw, equatorial_stars, observer):
        super().__init__()
        self.data_for_draw = data_for_draw
        self.observer = observer
        self.data_in_picture = dict()
        self.screen_stars = list()
        self.equatorial_coordinates = equatorial_stars
        self.data = Data().constellations
        x = float(self.observer.vector.z)
        y = math.sqrt(self.observer.vector.x**2+self.observer.vector.y**2)
        self.camera = Camera(x, y, 0)
        self.cp = QDesktopWidget().availableGeometry()
        self.create_window()

    def create_window(self):
        self.resize(self.cp.width(), self.cp.height())
        self.setWindowTitle('Sky')
        self.setStyleSheet('background-color:black;')
        self.image = QImage(self.width(), self.height(), QImage.Format_ARGB32)
        self.image.fill(Qt.black)
        self.setMouseTracking(True)
        self.menu = Menu(self.observer, self.changed_observer)
        self.get_sides()
        self.show()

    def changed_observer(self):
        self.observer = Observer(self.menu.longitudeEdit.text(),
                                 self.menu.latitudeEdit.text(),
                                 self.menu.angle_of_observeEdit.text(),
                                 self.menu.vector_of_watchEdit.text(),
                                 self.menu.timeEdit.text())
        self.camera.angle_of_rotation_x = -self.observer.vector.z
        summa = self.observer.vector.x**2 + self.observer.vector.y**2
        self.camera.angle_of_rotation_y = math.sqrt(summa)
        self.data_for_draw = []
        for equatorial in self.equatorial_coordinates:
            horizontal = equatorial[0].equatorial_to_horizontal(self.observer)
            point_3d = horizontal.horizontal_to_cartesian()
            self.data_for_draw.append(
                Info(point_3d, equatorial[1].color,
                     equatorial[1].radius, equatorial[1])
            )
        self.screen_stars = []
        self.showing()

    def find_star_on_screen(self, x, y):
        for tool_tip, screen in self.data_in_picture.items():
            if int(screen.x) - screen.radius <= x\
                    <= int(screen.x) + screen.radius \
                    and int(screen.y) - screen.radius <= y\
                    <= int(screen.y) + screen.radius:
                return tool_tip, screen.constellation

    def mouseMoveEvent(self, mouse_event):
        result = self.find_star_on_screen(mouse_event.x(), mouse_event.y())
        if result is not None:
            tool_tip, constellation = result
            QToolTip\
                .showText(QPoint(mouse_event.globalX(),
                                 mouse_event.globalY()),
                          tool_tip)
            self._change_rotation_angle(0, 0, 0)
            self.draw_stars_and_sides_on_picture(constellation, 50)
        else:
            QToolTip.hideText()
            self._change_rotation_angle(0, 0, 0)
            self.draw_stars_and_sides_on_picture()

    def get_zoom(self, angle):
        self.observer.angle += angle
        input_angle = self.observer.input_angle.split(':')
        s = ':' + input_angle[1] + ':' + input_angle[2]
        input_angle = str(int(input_angle[0]) + angle) + s
        self.observer.input_angle = input_angle
        self.menu.angle_of_observeEdit.setText(self.observer.input_angle)
        self.screen_stars = []
        self.showing()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Plus:
            if self.observer.angle >= 10:
                self._change_rotation_angle(0, 0, 0)
                self.get_zoom(-1)
        if event.key() == Qt.Key_Minus:
            if self.observer.angle <= 90:
                self._change_rotation_angle(0, 0, 0)
                self.get_zoom(1)
        if event.key() == Qt.Key_R:
            self._change_rotation_angle(0, 0, 1)
            self.get_zoom(0)
        if event.key() == Qt.Key_G:
            self._change_rotation_angle(0, 0, -1)
            self.get_zoom(0)
        if event.key() == Qt.Key_D:
            self._change_rotation_angle(0, -1, 0)
            self.observer.vector.y += 1
            self.get_zoom(0)
        if event.key() == Qt.Key_A:
            self._change_rotation_angle(0, 1, 0)
            self.observer.vector.y -= 1
            self.get_zoom(0)
        if event.key() == Qt.Key_W:
            self._change_rotation_angle(-1, 0, 0)
            self.observer.vector.x -= 1
            self.get_zoom(0)
        if event.key() == Qt.Key_S:
            self._change_rotation_angle(1, 0, 0)
            self.observer.vector.x += 1
            self.get_zoom(0)
        if event.key() == Qt.Key_M:
            self.menu.show()

    def give_screen_stars(self):
        for star in self.data_for_draw:
            color, radius = star.color, star.radius
            if self.camera.angle_of_rotation_z != 0:
                star.point3d.x, star.point3d.y, star.point3d.z \
                    = self.camera.rotate_z(star.point3d)
            if self.camera.angle_of_rotation_y != 0:
                star.point3d.x, star.point3d.y, star.point3d.z\
                    = self.camera.rotate_y(star.point3d)
            if self.camera.angle_of_rotation_x != 0:
                star.point3d.x, star.point3d.y, star.point3d.z\
                    = self.camera.rotate_x(star.point3d)
            point2d = star.point3d.cartesian_to_screen(self.observer)
            x, y = point2d.x*300+self.width()/2, point2d.y*300+self.height()/2
            tool_tip = 'constellation: ' + \
                       self.data[star.star.constellation] + \
                       '\n' + 'spectral class: ' + \
                       star.star.spectral_class+'\n' + \
                       'apparent magnitude: ' + \
                       str(star.star.apparent_magnitude)
            self.data_in_picture[tool_tip] = Screen(x, y,
                                                    radius,
                                                    star.star.constellation)
            self.screen_stars.append(Point2d(x, y,
                                             color, radius,
                                             star.star.constellation))

    def draw_stars_and_sides_on_picture(self, constellation='', alpha=255):
        self.image.fill(Qt.black)
        painter = QPainter(self.image)
        for star in self.screen_stars:
            color = QColor(star.color)
            if constellation != '' and constellation != star.constellation:
                color.setAlpha(alpha)
            painter.setPen(QPen(color))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(star.x, star.y, star.radius, star.radius)
        self._draw_sides(painter, alpha)
        self.repaint()

    def _draw_sides(self, painter, alpha=255):
        for side in self.sides:
            color = QColor(side.color)
            color.setAlpha(alpha)
            painter.setPen(QPen(color, 1, Qt.SolidLine))
            if side.name == 'north':
                side.coordinates.x += self.camera.angle_of_rotation_y*3
            if side.name == 'south':
                side.coordinates.x -= self.camera.angle_of_rotation_y*3
            if side.name == 'west':
                side.coordinates.y -= self.camera.angle_of_rotation_y*3
            if side.name == 'east':
                side.coordinates.y += self.camera.angle_of_rotation_y*3
            painter.drawLine(side.coordinates.x, side.coordinates.y,
                             self.width()//2, self.height()//2)

    def get_sides(self):
        self.sides = list()
        width, height = self.width(), self.height()
        self.sides.append(Side('north', sky_coordinate_systems
                               .Screen(width//2, 0), '#000080'))
        self.sides.append(Side('south', sky_coordinate_systems
                               .Screen(width//2, height), '#00FF00'))
        self.sides.append(Side('west', sky_coordinate_systems
                               .Screen(0, height//2), '#FF0000'))
        self.sides.append(Side('east', sky_coordinate_systems
                               .Screen(width, height//2), '#FFFFFF'))

    def showing(self):
        self.give_screen_stars()
        self.draw_stars_and_sides_on_picture()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def _change_rotation_angle(self, x, y, z):
        if x != self.camera.angle_of_rotation_x:
            self.camera.angle_of_rotation_x = x
        if y != self.camera.angle_of_rotation_y:
            self.camera.angle_of_rotation_y = y
        if z != self.camera.angle_of_rotation_z:
            self.camera.angle_of_rotation_z = z
