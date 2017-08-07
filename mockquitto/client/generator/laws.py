from abc import ABCMeta, abstractmethod
import random


class LawGeneration(metaclass=ABCMeta):
    @abstractmethod
    def get_next(self):
        pass


class Random(LawGeneration):
    def __init__(self, start_value, range_value):
        if isinstance(range_value, (list, tuple)) and len(range_value) == 2:
            self.start_value = start_value + range_value[0] if range_value[0] < 0 else start_value - range_value[0]
            self.end_value = start_value + range_value[1]
        else:
            self.start_value = start_value
            self.end_value = start_value + range_value
        self.is_random = True
        self.random_generator = self.create_random_generator()

        self._last_generated = None

    def get_next(self):
        return next(self.random_generator)

    def create_random_generator(self):
        while self.is_random is True:
            self._last_generated = self.get_random()
            yield self._last_generated
        yield self._last_generated

    @abstractmethod
    def get_random(self):
        pass


class RandomInteger(Random):
    def get_random(self):
        return random.randint(self.start_value, self.end_value)


class RandomReal(Random):
    def get_random(self):
        return random.uniform(self.start_value, self.end_value)
