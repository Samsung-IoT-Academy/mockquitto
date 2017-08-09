from mockquitto.client.generator import Generator
from mockquitto.client.devices import Device
from mockquitto.client.devices.values import Luxes as LuxValue

class LuminocityDevice(Device):
    def __init__(self, generator: Generator, dev_name=None, **kwargs):
        fmt_str = "\"{{'data': {{'luminocity': {lum}}}, 'status': {{'devEUI': '807B85902000016D', " \
                  "'rssi': -15, 'temperature': -10, 'battery': 3250, 'date': {date_mqtt_fmt}}}}}\""
        super().__init__(generator=generator, format_str=fmt_str, dev_name=dev_name, **kwargs)
        self._value_cls = LuxValue

    def format_out(self, value: LuxValue):
        if isinstance(value, self._value_cls):
            return self._fmt_str.format(lum=value.value)
        else:
            raise ValueError