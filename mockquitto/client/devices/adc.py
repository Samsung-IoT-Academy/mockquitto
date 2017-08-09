from mockquitto.client.generator import Generator
from mockquitto.client.devices import Device
from mockquitto.client.devices.values import MilliVolts as mV

class ADCDevice(Device):
    def __init__(self, generator: Generator, dev_name=None, dev_num=0, **kwargs):
        fmt_str = "\"adc{num}\":{{mv}}".format(num=dev_num)
        super().__init__(generator=generator, format_str=fmt_str, dev_name=dev_name, dev_num=dev_num, **kwargs)
        self._value_cls = mV

    def format_out(self, value: mV):
        if isinstance(value, self._value_cls):
            return self._fmt_str.format(mv=value.value)
        else:
            raise ValueError
