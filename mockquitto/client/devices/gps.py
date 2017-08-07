from mockquitto.client.generator import Generator

from mockquitto.client.devices.device import Device
from mockquitto.client.devices.values import GPSCoordinates


class GPS(Device):
    def __init__(self, generator: Generator, accuracy=4):
        fmt_str = "\"lat\":{{0:.{0}f}},\"lon\":{{1:.{1}f}}".format(accuracy, accuracy)
        super().__init__(generator=generator, format_str=fmt_str)
        self._value_cls = GPSCoordinates
        self._accuracy = accuracy

    def format_out(self, value: GPSCoordinates):
        if isinstance(value, GPSCoordinates):
            return self._fmt_str.format(value.lat, value.lon)
        else:
            raise ValueError