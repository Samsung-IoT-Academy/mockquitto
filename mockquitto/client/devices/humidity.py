from mockquitto.client.generator import Generator
from mockquitto.client.devices import Device
from mockquitto.client.devices.values import Humidity as HumidityValue

class HumidityDevice(Device):
    def __init__(self, generator: Generator):
        fmt_str = "\"humidity\":{hum:d}"
        self._dict_repr = {
            'humidity': self._value.value
        }
        super().__init__(generator=generator, format_str=fmt_str)
        self._value_cls = HumidityValue

    def format_out(self, value: HumidityValue):
        if isinstance(value, self._value_cls):
            return self._fmt_str.format(hum=value.value)
        else:
            raise ValueError