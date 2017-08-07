class GPSCoordinates:
    permissible_indexes = (0, 1)

    def __init__(self, lat, lon=None, *args):
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            self.lat = lat
            self.lon = lon
        elif isinstance(lat, list):
            self.lat = lat[0]
            self.lon = lat[1]

        self._dict = {
            0: self.lat,
            1: self.lon
        }

    def tuplize(self):
        return self.lat, self.lon

    def __getitem__(self, item):
        if item not in self.permissible_indexes:
            raise IndexError
        elif not isinstance(item, int):
            raise TypeError
        else:
            return self._dict.get(item)
