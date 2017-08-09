from abc import ABCMeta, abstractmethod


from mockquitto.client.generator import Generator, ValuePair


class Device(metaclass=ABCMeta):
    """
    Base device class gives method to implement by its subclasses

    Attributes:
        format_str -- format of json string
        freq_type -- time between generations of messages, may be constant or random
    """

    def __init__(self, format_str=None, generator: Generator=None, dev_name=None, topic=None, *, field_holder=None,
                 dev_num=0):
        """

        :param format_str: string for formatting messages
        :param generator: object, which generates number
        """
        self._fmt_str = format_str
        self.generator = generator
        self._name = dev_name
        self._field_holder = field_holder
        self._dev_num = dev_num

        self._gen_obj = self.generator_func()
        self._value = None
        self._mqtt_topic = topic

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def gen_obj(self):
        return self._gen_obj

    @property
    def format_string(self) -> str:
        return self._fmt_str

    @property
    def field_holder(self) -> str:
        return self._field_holder

    @property
    def dev_num(self) -> int:
        return self._dev_num

    @property
    def mqtt_topic(self) -> str:
        if self._mqtt_topic is None:
            raise ValueError
        return self._mqtt_topic

    def generator_func(self):
        for value_pair in self.generator.get_gen_obj():
            self._value = value_pair.value
            return_type, return_obj = yield
            if return_type is str and return_obj is tuple:
                yield (value_pair.time, self.format_out(value_pair.value))
            elif return_type is dict and return_obj is tuple:
                yield (value_pair.time, value_pair.value.dictify())
            elif return_type is str and return_obj is ValuePair:
                yield ValuePair(value_pair.time, self.format_out(value_pair.value))
            elif return_type is dict and return_obj is ValuePair:
                yield ValuePair(value_pair.time, value_pair.value.dictify())
            else:
                raise StopIteration

    def get(self, return_type: type = str, return_obj: type = tuple):
        next(self._gen_obj)
        return self._gen_obj.send((return_type, return_obj))

    @abstractmethod
    def format_out(self, value):
        pass
