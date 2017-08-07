import random
from abc import ABCMeta, abstractmethod
from enum import Enum

from mockquitto.client.exceptions import GeneratorCreationError
from mockquitto.client.generator.laws import LawGeneration


class FrequencyType(Enum):
    CONSTANT = 0
    RANDOM = 1


class GenerationType(Enum):
    FINITE = 0
    INFINITE = 1


class ValuePair:
    """
    Wrapper for return values

    Attributes:
        time: time for sleep (for asyncio event loop)
        value: returning value
    """
    permissible_indexes = (0, 1)

    def __init__(self, time, value):
        self.time = time
        self.value = value
        self._dict = {
            0: self.time,
            1: self.value
        }

    def __getitem__(self, item):
        if item not in self.permissible_indexes:
            raise IndexError
        elif not isinstance(item, int):
            raise TypeError
        else:
            return self._dict.get(item)


class Generator(metaclass=ABCMeta):
    """
    Base generator object for generating values
    """
    def __init__(self, start_value, gen_law,
                 freq_type: FrequencyType=FrequencyType.CONSTANT, **kwargs):
        """
        Initializing Generator object

        :param start_value:
        :param gen_law: tuple, list of LawGeneration derived objects or one instance of it
        :param freq_type:
        :param kwargs:
        """
        self.gen_law_list = gen_law if isinstance(gen_law, (list, tuple)) else tuple(gen_law)
        self.start_value = start_value
        self.freq_type = freq_type
        if freq_type is FrequencyType.CONSTANT and 'freq_value' in kwargs:
            self.freq_value = kwargs['freq_value']
        elif freq_type is FrequencyType.RANDOM and 'freq_range' in kwargs:
            self.freq_range = kwargs['freq_range']
        else:
            raise GeneratorCreationError()

        self._generation_flag = False
        self._generator_obj = self._generator_impl()
        self._value_cls = self.start_value.__class__

    @abstractmethod
    def _generator_impl(self):
        pass

    def get_gen_obj(self):
        return self._generator_obj

    def next(self):
        return next(self._generator_obj)

    def stop(self):
        self._generation_flag = False

    def delay(self):
        if self.freq_type is FrequencyType.CONSTANT:
            return self.freq_value
        elif self.freq_type is FrequencyType.RANDOM:
            return random.uniform(*self.freq_range)

    def get_value_pair(self) -> ValuePair:
        return ValuePair(self.delay(), self._value_cls([gen_law.get_next() for gen_law in self.gen_law_list]))


class GeneratorFinite(Generator):
    def __init__(self, start_value, gen_law, *args, **kwargs):
        super().__init__(start_value, gen_law, *args, **kwargs)
        self._gen_type = GenerationType.FINITE
        self._stop_value = kwargs.get('stop_value')
        self._iters = kwargs.get('iters')

    def _generator_impl(self):
        if self._stop_value:
            value = self.get_value_pair()
            yield value[1]
            while value[1] != self._stop_value and self._generation_flag:
                value = self.get_value_pair()
                yield value
        elif self._iters:
            for x in range(self._iters):
                yield self.get_value_pair()


class GeneratorInfinite(Generator):
    def __init__(self, start_value, gen_law, *args, **kwargs):
        super().__init__(start_value, gen_law, *args, **kwargs)
        self._gen_type = GenerationType.INFINITE

    def _generator_impl(self):
        self._generation_flag = True
        while self._generation_flag:
            yield self.get_value_pair()
