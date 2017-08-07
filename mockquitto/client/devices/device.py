from abc import ABCMeta, abstractmethod
import asyncio

from mockquitto.client.generator import Generator


class Device(metaclass=ABCMeta):
    """
    Base device class gives method to implement by its subclasses

    Attributes:
        format_str -- format of json string
        freq_type -- time between generations of messages, may be constant or random
        gen_law -- function by which values is generating
        gen_type -- type of generator, may be infinite or finite
        start_value -- starting value
        stop_value -- stopping value, important for monotonic GenLaws
        iters -- number of iterations
    """

    def __init__(self, format_str=None, generator: Generator=None,
                 start_value=None, stop_value=None, iters=None):
        """

        :param format_str: string for formatting messages
        :param generator: object, which generates number
        :param start_value: starting value
        :param stop_value: stopping value
        :param iters: number of iterations
        """
        self._fmt_str = format_str
        self.generator = generator

        self._start_value = start_value
        self._stop_value = stop_value
        self._iter_nums = iters

        self._gen_obj = self._get_gen_obj()

    def _get_gen_obj(self):
        for value_pair in self.generator.get_gen_obj():
            print(value_pair.time)
            yield (value_pair.time, self.format_out(value_pair.value))

    def get(self):
        return next(self._gen_obj)

    @abstractmethod
    def format_out(self, value):
        pass
