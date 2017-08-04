from abc import ABCMeta, abstractmethod
import asyncio

from mockquitto.client.exceptions import DeviceCreationError
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

    def __init__(self,
                 format_str=None,
                 generator: Generator=None,
                 start_value=None, stop_value=None, iters=None):
        """

        :param format_str: string for formatting messages
        :param generator: generator-like object
        :param start_value: starting value
        :param stop_value: stopping value
        :param iters: number of iterations
        """
        self._fmt_str = format_str
        self._generator = generator

        if gen_type is GenerationType.FINITE and (stop_value is None or iters is None):
            raise DeviceCreationError(Msg="Finite device must have stop value or number of iterations!")
        elif gen_type is GenerationType.INFINITE and stop_value is not None:
            raise DeviceCreationError(Msg="Infinite device must not have stop value!")

        self._start_value = start_value
        self._stop_value = stop_value
        self._iter_nums = iters

    @abstractmethod
    @asyncio.coroutine
    def get(self):
        for value_pair in self._generator.next():
            yield (value_pair.time, self.format_out(value_pair.values))

    @abstractmethod
    def format_out(self):
        pass