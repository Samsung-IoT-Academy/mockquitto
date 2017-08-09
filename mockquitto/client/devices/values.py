from sys import maxsize

MAX_INT = maxsize


class GPSCoordinates:
    permissible_indexes = (0, 1)
    valuable_fields = ("lat", "lon")

    def __init__(self, lat, lon=None):
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

    def __getitem__(self, item):
        if item not in self.permissible_indexes:
            raise IndexError
        elif not isinstance(item, int):
            raise TypeError
        else:
            return self._dict.get(item)

    def tuplize(self):
        return self.lat, self.lon

    def dictify(self):
        return {key: vars(self)[key] for key in vars(self).keys() if key in self.valuable_fields}


class SingleValue:
    possible_range = {
        'min': None,
        'max': None
    }
    field_name = ""

    def __init__(self, value):
        if isinstance(value, (int, float)):
            self.value = value
        elif isinstance(value, list):
            self.value = value[0]

        if self._checking_range(self.value) is False:
            raise ValueError

    def __getitem__(self, item):
        self._dict = {}
        if item != 0:
            raise IndexError
        elif not isinstance(item, int):
            raise TypeError
        else:
            return self.value

    def _checking_range(self, value_to_check):
        return True if (self.possible_range['max'] >= value_to_check >= self.possible_range['min']) else False

    def tuplize(self):
        return tuple(self.value)

    def dictify(self):
        return {self.field_name: self.value}


class Humidity(SingleValue):
    possible_range = {
        'min': 0,
        'max': 100
    }
    field_name = "humidity"


class Temperature(SingleValue):
    possible_range = {
        'min': -273,
        'max': 105
    }
    field_name = "temperature"

    def to_kelvins(self):
        return self.value + 273

    def to_farenheit(self):
        return self.value * 1.8 + 32

    def to_celsius(self):
        return self.value


class Luxes(SingleValue):
    possible_range = {
        'min': 0,
        'max': MAX_INT
    }


class MilliVolts(SingleValue):
    possible_range = {
        'min': 0,
        'max': 5000
    }
    field_name = "millivolts"