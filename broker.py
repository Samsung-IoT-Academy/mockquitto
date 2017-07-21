#! /usr/bin/env python

import signal
import errno
import socket
import logging
import functools
import asyncio

from hbmqtt.broker import Broker


class BrokerConfig:
    def __init__(self, proto='tcp', domain='localhost', port=1883, max_conns=10, interval=10):
        self.__proto = proto
        self.__domain = domain
        self.__port = self.broker_port(port)
        self.__max_conns = max_conns
        self.__interval = interval


    def get_config(self):
        return {
            'listeners': {
                'default': {
                    'type': self.__proto,
                    'bind': self.__domain + ':' + str(self.__port),
                    'max_connections': self.__max_conns,
                }
            },
            'sys_interval': self.__interval
        }

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    def broker_port(self, port=1883):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                s.bind(('localhost', port))
            except OSError as err:
                if err.errno == errno.EADDRINUSE:
                    port += 1
                continue
            break
        addr, port = s.getsockname()
        s.close()
        return port


@asyncio.coroutine
def broker_coro(broker, config):
    yield from broker.start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    logger = logging.getLogger(name="MQTT-Broker")

    config = BrokerConfig()
    broker = Broker(config.get_config())

    loop = asyncio.get_event_loop()

    loop.run_until_complete(broker_coro(broker, config))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(broker.shutdown())
    finally:
        logger.info("Closing")
        loop.close()
