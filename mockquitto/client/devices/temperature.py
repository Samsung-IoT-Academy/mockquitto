from mockquitto.client.generator import Generator
from mockquitto.client.devices import Device
from mockquitto.client.devices.values import Temperature as TemperatureValue

class TemperatureDevice(Device):
    def __init__(self, generator: Generator, dev_name=None, **kwargs):
        fmt_str = "\"temperature\":{temp:d}"
        super().__init__(generator=generator, format_str=fmt_str, dev_name=dev_name, **kwargs)
        self._value_cls = TemperatureValue

    def format_out(self, value: TemperatureValue):
        if isinstance(value, self._value_cls):
            return self._fmt_str.format(temp=value.value)
        else:
            raise ValueError