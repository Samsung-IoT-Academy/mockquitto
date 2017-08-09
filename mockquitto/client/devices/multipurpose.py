from abc import ABCMeta, abstractmethod
from datetime import datetime
from functools import reduce
from json import JSONEncoder
from copy import deepcopy

from mockquitto.utils import merge_dicts, stringify_dict_open
from mockquitto.client.generator import ValuePair
from mockquitto.client.exceptions import DeviceCreationError
from .device import Device
from .temperature import TemperatureDevice
from .humidity import HumidityDevice
from .adc import ADCDevice


class MultiDevice(metaclass=ABCMeta):
    def __init__(self, devices, topic, format_str=None):
        if isinstance(devices, (list, tuple)) and all(isinstance(item, Device) for item in devices):
            if len({d.name: d for d in devices}.keys()) == len(devices):
                self.device_list = devices
            else:
                raise DeviceCreationError(msg="All device names must be unique in one multidevice")
        else:
            raise DeviceCreationError(msg="Devices must be iterable object of Device class of its derivative")

        self._fmt_str = format_str
        self._values = None
        self._mqtt_topic = topic

    @property
    def mqtt_topic(self) -> str:
        if self._mqtt_topic is None:
            raise ValueError
        return self._mqtt_topic

    def get(self):
        value_pair = ValuePair()
        for device in self.device_list:
            value_pair += device.get(return_type=dict, return_obj=ValuePair)

        return value_pair.time / len(value_pair.value), self.format_out(value_pair.value)

    @abstractmethod
    def format_out(self, value) -> str:
        pass


class TempHumDevice(MultiDevice):
    TMP_GEN_NAME = "Temperature"
    HMD_GEN_NAME = "Humidity"

    def __init__(self, generators, topic: str):
        temp_generator = next((gnrtr for gnrtr in generators if gnrtr.name == self.TMP_GEN_NAME), None)
        humd_generator = next((gnrtr for gnrtr in generators if gnrtr.name == self.HMD_GEN_NAME), None)
        if temp_generator is None or humd_generator is None:
            raise DeviceCreationError(msg="Generators name must have name properties {} and {} respectevly".format(
                self.TMP_GEN_NAME, self.HMD_GEN_NAME
            ))
        devices = TemperatureDevice(generator=temp_generator, dev_name="Temperature_1"),\
                  HumidityDevice(generator=humd_generator, dev_name="Humidity_1")
        fmt_str = "\"{{'data': {values_open_dict} 'pressure': 977}}, 'status': {{'devEUI': '807B85902000016D', " \
                  "'rssi': -15, 'temperature': -10, 'battery': 3250, 'date': {date_mqtt_fmt}}}}}\""
        super().__init__(devices=devices, format_str=fmt_str, topic=topic)

    def format_out(self, value) -> str:
        fmt = self._fmt_str.format(values_open_dict=stringify_dict_open(merge_dicts(value[0], value[1])),
                             date_mqtt_fmt=datetime.utcnow().isoformat() + "Z")
        return fmt


class MultichannelDevice(MultiDevice):
    def __init__(self, devices, topic, format_str=None):
        super().__init__(devices, topic, format_str)
        self._value_cls = devices[0].generator.value_cls
        self._value_dict = {}

    def get(self):
        accum_time = 0
        for device in self.device_list:
            time, value = device.get(return_type=dict, return_obj=tuple)
            accum_time += time
            print(device.field_holder + str(device.dev_num))
            self._value_dict[device.field_holder + str(device.dev_num)] = value[self._value_cls.field_name]

        print(self._value_dict)
        return accum_time / len(self.device_list), self.format_out()

    def format_out(self, value):
        pass


class MultichannelADC(MultichannelDevice):
    def __init__(self, generators, topic: str):
        devices = [ADCDevice(generator=g, dev_name=g.name, dev_num=num, field_holder="adc")
                   for g, num in zip(generators, range(1, len(generators)+1))]
        fmt_str = "\"{{'data': {values_dict}, 'status': {{'devEUI': '807B85902000016D', " \
                  "'rssi': -15, 'temperature': -10, 'battery': 3250, 'date': {date_mqtt_fmt}}}}}\""
        super().__init__(devices=devices, format_str=fmt_str, topic=topic)
        self._schema = {
            'data': None,
            'status': {
                'devEUI': '807B85902000016D',
                'rssi': -15,
                'temperature': -10,
                'battery': 3250,
                'date': None
            }
        }

    def format_out(self, value=None) -> str:
        """

        :param value: list of formatted string
        :return:
        """
        if value is None:
            return JSONEncoder().encode(self.update_schema())
        else:
            return self._fmt_str.format(values_dict="{" + ", ".join(value) + "}",
                             date_mqtt_fmt=datetime.utcnow().isoformat() + "Z")

    def update_schema(self):
        obj = deepcopy(self._schema)
        obj['data'] = self._value_dict
        obj['status']['date'] = datetime.utcnow().isoformat() + "Z"
        return obj