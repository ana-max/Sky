from visualization.observer import Observer
import argparse
import sys
from PyQt5.QtWidgets import QApplication
from visualization.stars_window import StarsWindow
from stars_parser import Parser
import datetime


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-long', '--longitude', default='00:00:00',
                        help='Enter the longitude of observer.'
                             'Format: d:m:s where '
                             'd - degrees, m - minutes, s - seconds.'
                             'Default is 00:00:00 - Prime Meridian')
    parser.add_argument('-lat', '--latitude', default='00:00:00',
                        help='Enter the latitude of observer.'
                             'Format: d:m:s, where '
                             'd - degrees, m - minutes, s - seconds.'
                             'Default is 00:00:00 - Zero Parallel')
    parser.add_argument('-a', '--angle', default='35:00:00',
                        help='Enter the angle to observe.'
                             'Format: d:m:s, where '
                             'd - degrees, m - minutes, s - seconds.'
                             'Default is 35:00:00')
    parser.add_argument('-t', '--time', default=datetime.datetime.now(),
                        help='Enter the time of observer.'
                             'Format: h:m:s, where '
                             'h - hours, m - minutes, s - seconds.'
                             'Default is now')
    parser.add_argument('-c', '--constellations', default='',
                        help='Enter the constellations what you want to see.'
                             'Default is all.')
    parser.add_argument('-v', '--vector', default='(0,0,0)',
                        help='Enter the vector to observe.'
                             'Format: (x,y,z) , where '
                             'd - degrees, m - minutes, s - seconds.'
                             'Default is (0,0,0)')
    return parser.parse_args()


def main():
    p = parse_arguments()
    observer = Observer(p.longitude, p.latitude, p.angle, p.vector, p.time)
    data_of_stars, eq = Parser().give_stars(observer, p.constellations)
    app = QApplication(sys.argv)
    window = StarsWindow(data_of_stars, eq, observer)
    window.draw_stars_and_sides_on_picture()
    window.showing()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
