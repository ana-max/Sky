
colors = {'O': '#20B2AA', 'B': '#66CDAA', 'A': '#FFFFFF', 'C': '#FFDAB9',
          'S': '#FFE4B5	', 'N': '#4682B4', 'R': '#FFA07A',
          'F': '#FFFFFF', 'G': '#F0E68C', 'K': '#F0E68C', 'M': '#FF6347'}

stars_radius = {1: 14, 2: 12, 3: 10, 4: 8, 5: 6, 6: 4, 7: 2}


class Star:
    def __init__(self, right_ascension, decline,
                 apparent_magnitude, spectral_class, constellation):
        self._right_ascension = right_ascension
        self._decline = decline
        self._apparent_magnitude = float(apparent_magnitude)
        self._spectral_class = spectral_class.strip()
        self._constellation = constellation
        self.text_for_tool_tip = str(right_ascension)

    @property
    def right_ascension(self):
        return self._right_ascension

    @property
    def decline(self):
        return self._decline

    @property
    def spectral_class(self):
        return self._spectral_class

    @property
    def apparent_magnitude(self):
        return self._apparent_magnitude

    @property
    def color(self):
        return self._get_color()

    @property
    def radius(self):
        return self._get_radius()

    @property
    def constellation(self):
        return self._constellation

    def _get_color(self):
        sym = self.spectral_class[0]
        i = 1
        if sym == 'f':
            sym = 'F'
        while sym.islower() or not sym.isalpha():
            sym = self.spectral_class[i]
            i += 1
        return colors[sym]

    def _get_radius(self):
        keys = stars_radius.keys()
        for key in keys:
            if self.apparent_magnitude <= key:
                return stars_radius[key]

    def is_never_visible(self):
        return self.apparent_magnitude >= 6.5
