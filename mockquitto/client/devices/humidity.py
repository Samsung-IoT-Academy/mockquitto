from mockquitto.client.generator import Generator
from mockquitto.client.devices import Device
from mockquitto.client.devices.values import Humidity as HumidityValue

class HumidityDevice(Device):
    def __init__(self, generator: Generator, dev_name=None, **kwargs):
        fmt_str = "\"humidity\":{hum:d}"
        super().__init__(generator=generator, format_str=fmt_str, dev_name=dev_name, **kwargs)
        self._value_cls = HumidityValue

    def format_out(self, value: HumidityValue):
        if isinstance(value, self._value_cls):
            return self._fmt_str.format(hum=value.value)
        else:
            raise ValueError