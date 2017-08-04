import random
from abc import ABCMeta, abstractmethod
from enum import Enum

from mockquitto.client.exceptions import GeneratorCreationError
from mockquitto.client.generator.laws import LawGeneration


class FrequencyType(Enum):
    _order_ = 'CONSTANT RANDOM'
    CONSTANT = 0
    RANDOM = 1


class GenerationType(Enum):
    FINITE = 0
    INFINITE = 1


class Generator(metaclass=ABCMeta):
    def __init__(self, start_value, gen_law: LawGeneration, freq_type: FrequencyType=FrequencyType.CONSTANT, **kwargs):
        self._gen_law = gen_law
        self._start_value = start_value
        self._freq_type = freq_type
        if freq_type is FrequencyType.CONSTANT and 'freq_value' in kwargs:
            self._freq_value = kwargs['freq_value']
        elif freq_type is FrequencyType.RANDOM and 'freq_range' in kwargs:
            self._freq_range = kwargs['freq_range']
        else:
            raise GeneratorCreationError()

        self._generation_flag = False

    @abstractmethod
    def next(self):
        pass

    def delay(self):
        if self._freq_type is FrequencyType.CONSTANT:
            return self._freq_value
        elif self._freq_type is FrequencyType.RANDOM:
            return random.uniform(*self._freq_range)

    def get_value_tuple(self):
        return (self.delay(), self._gen_law.get())


class GeneratorFinite(Generator):
    def __init__(self, start_value, gen_law: LawGeneration, *args, **kwargs):
        super().__init__(start_value, gen_law, *args, **kwargs)
        self._gen_type = GenerationType.FINITE
        self._stop_value = kwargs.get('stop_value')
        self._iters = kwargs.get('iters')

    def next(self):
        if self._stop_value:
            value_tuple = self.get_value_tuple()
            yield
            while value_tuple[1] != self._stop_value and self._generation_flag:
                value_tuple = self.get_value_tuple()
                yield value_tuple
        elif self._iters:
            for x in range(self._iters):
                yield self.get_value_tuple()


class GeneratorInfinite(Generator):
    def __init__(self, start_value, gen_law: LawGeneration, *args, **kwargs):
        super().__init__(start_value, gen_law, *args, **kwargs)
        self._gen_type = GenerationType.INFINITE

    def next(self):
        self._generation_flag = True
        while self._generation_flag:
            yield self.get_value_tuple()