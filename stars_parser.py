import os
from visualization.star import Star
from collections import namedtuple
from astronomical_calculations.sky_coordinate_systems import Equatorial
from bs4 import BeautifulSoup
import ftplib
import re
import zipfile
Info = namedtuple('Info', 'point3d color radius star')
reg_for_bright_stars = re.compile(r'([\d][\d]*)[\s]+([\d\s]*:[\d\s]*:[\d.\s]*)'
                                  r'\s([+\-\d\s]*:[\d\s]*:[\s]*[\d.]*)'
                                  r'[\s]+([\d]+.[\d]+)[\s]+([\d+\-]+.[\d]+)'
                                  r'[\s]([\w|\s][\w|\s])[\s|\-]([\d]+.[\d]+)'
                                  r'[\s]([\s\w.,:()\-+*?/]{20})[\s]+'
                                  r'([\d.+\-]+)[\s]+([\d.+\-]+)[\s]([\s\w]+)'
                                  r'[\s]([\d+\-]+)[\s]+([[\d]+)[\s]'
                                  r'([\d|\s]{3})([\w|\s]{4})(.*[\s])')

reg_for_double_stars = re.compile(r'([\d][\d]*)[\s]+([\d\s]*:[\d\s]*.[\d\s]*)'
                                  r'\s([+\-\d\s]*:[\s]*[\d.]*)[\s]+'
                                  r'([A-Za-z\-\s]+)([\d|\s]{4})'
                                  r'[\s]([\d|\s]{4})[\s]([\d|\s]{3})'
                                  r'[\s]([\d|\s]{3})[\s]([\d|\s|\.]{5})[\s]'
                                  r'([\d|\s|\.]{7})[\s]([\d|\s|\.]{4})'
                                  r'[\s]([\d|\s|\.]{4})[\s]'
                                  r'([\s\w.,:()\-\+\*\?\/]{9})[\s]'
                                  r'([\d|\s|\+|\-]{5})'
                                  r'[\s]([\d|\s|\+|\-]{5})[\s]([\w|\s])[\s]'
                                  r'(.*)')


class Parser:
    @staticmethod
    def download_and_unpack_the_archive():
        with ftplib.FTP(r'shannon.usu.edu.ru') as ftp:
            ftp.login('anonymous', 'email@email.com')
            ftp.cwd(r'perl/data/')
            ftp.retrbinary('RETR stars.zip', open('stars.zip', 'wb').write)
        with zipfile.ZipFile('stars.zip') as z_file:
            z_file.extractall()

    @staticmethod
    def _get_into_data(star, observer, data_for_draw):
        equatorial = (Equatorial(star.right_ascension, star.decline), star)
        horizontal = equatorial[0].equatorial_to_horizontal(observer)
        point_3d = horizontal.horizontal_to_cartesian()
        data_for_draw.append(
            Info(point_3d, star.color, star.radius, star)
        )
        return data_for_draw, equatorial

    def give_all_constellations(self, constellations):
        wanted_constellations = constellations.split('_')
        self.download_and_unpack_the_archive()
        files = os.listdir('stars')
        data = []
        for constellation in wanted_constellations:
            count = 0
            for file in files:
                if file.endswith(constellation + '.htm'):
                    count += 1
                    data.append('stars/' + file)
            if count == 0:
                raise ValueError('There is no constellation ' + constellation)
        return data

    def give_stars(self, observer, constellation):
        constellations = self.give_all_constellations(constellation)
        data_for_draw = list()
        eq = list()
        for c in constellations:
            content = open(c)
            constellation = c.split('/')[1].split('.')[0]
            try:
                soup = BeautifulSoup(content, 'html.parser')
                bright = re.findall(reg_for_bright_stars, soup.prettify())
                double = re.findall(reg_for_double_stars, soup.prettify())
                data_for_draw, eq = self\
                    ._get_data_of_bright_stars(bright, observer,
                                               constellation, data_for_draw, eq)
                data_for_draw, eq = self.\
                    _get_data_of_double_stars(double, observer,
                                              constellation, data_for_draw, eq)
            except:
                pass
        return data_for_draw, eq

    def _get_data_of_bright_stars(self, bright, observer,
                                  constellation, data_for_draw, eq):
        for info in bright:
            right_ascension, decline, apparent_magnitude, spectral_class \
                = info[1], info[2], info[6], info[7]
            star = Star(right_ascension, decline,
                        apparent_magnitude, spectral_class, constellation)
            data_for_draw, equatorial = self\
                ._get_into_data(star, observer, data_for_draw)
            eq.append(equatorial)
        return data_for_draw, eq

    def _get_data_of_double_stars(self, double, observer,
                                  constellation, data_for_draw, eq):
        for info in double:
            right_ascension, decline = info[1], info[2]
            sp = right_ascension.split(' ')
            if sp[0] == '205':
                right_ascension = sp[1]
            apparent_magnitude = info[10] \
                if info[10].strip() != '' else info[11]
            spectral_class = info[12]
            if apparent_magnitude.strip() == '' \
                    or spectral_class.strip() == ''\
                    or spectral_class[0].isdigit():
                continue
            star = Star(right_ascension, decline,
                        apparent_magnitude, spectral_class, constellation)
            if star.is_never_visible():
                continue
            data_for_draw, equatorial = self\
                ._get_into_data(star, observer, data_for_draw)
            eq.append(equatorial)
        return data_for_draw, eq
