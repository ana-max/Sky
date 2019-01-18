
class Data:
    def __init__(self):
        self._constellations = dict()

    @property
    def constellations(self):
        return self.get_constellations()

    def get_constellations(self):
        with open('constellations.txt') as c:
            constellations = c.readlines()
            for constellation in constellations:
                constellation = constellation.split()
                if len(constellation) == 2:
                    self._constellations[constellation[1]] = constellation[0]
                else:
                    self._constellations[constellation[2]] \
                        = constellation[0] + ' ' + constellation[1]
        return self._constellations
