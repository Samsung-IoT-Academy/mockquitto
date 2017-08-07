import sys
import os
import signal
import asyncio
import argparse
import logging
import random

from hbmqtt.client import MQTTClient, ClientException, ConnectException
import hbmqtt.mqtt.constants as HBMQTT_CONST

from mockquitto.client.cli_utils import client_parser
from mockquitto.client.devices.gps import GPS
from mockquitto.client.generator.generator import GeneratorInfinite
from mockquitto.client.generator.laws import RandomReal
from mockquitto.client.devices.values import GPSCoordinates

TOPIC = 'devices/lora/807B85902000019A/gps'


class MQTTMockClient:

    _logger = None

    def __init__(self, port, period=1, logger_name="MQTT_Generator", loop=None, status=True):
        self._loop = asyncio.get_event_loop() if (loop is None) else loop
        self._status = status
        self._client = MQTTClient()
        self._broker_port = port
        self._period = period
        if MQTTMockClient._logger is None:
            MQTTMockClient._logger = logging.getLogger(logger_name)

        coords_gps = GPSCoordinates(55.4507, 37.3656)
        gen_law_list = RandomReal(coords_gps[0], (-1, 1)), RandomReal(coords_gps[1], (-1, 1))
        generator = GeneratorInfinite(coords_gps, gen_law_list, freq_value=0.5)
        self.device = GPS(generator)

    @property
    def client(self):
        return self._client

    def setup(self):
        @asyncio.coroutine
        def __internal_setup():
            try:
                yield from self._client.connect("mqtt://localhost:" + str(self._broker_port))
            except ConnectException:
                MQTTMockClient._logger.critical("Cannot connect to broker. Exit...")
                exit(0)

            yield from self._client.subscribe([
                (TOPIC, HBMQTT_CONST.QOS_1),
            ])

        try:
            self._loop.run_until_complete(__internal_setup())
        except KeyboardInterrupt:
            MQTTMockClient._logger.critical("Interrupted by user. Exit...")
            exit(0)

        return self._client

    def run(self):
        @asyncio.coroutine
        def __main():
            task_deliver = self._loop.create_task(self.deliver(self._client))
            task_send = self._loop.create_task(self.send(self._client))
            yield from task_deliver
            yield from task_send

        try:
            self._loop.run_until_complete(__main())
        except asyncio.CancelledError as err:
            MQTTMockClient._logger.debug("Catch the exception!")

    def clean(self):
        @asyncio.coroutine
        def __clean():
            yield from self._client.unsubscribe([TOPIC])
            yield from self._client.disconnect()
            yield from asyncio.sleep(0.5)

        try:
            self._loop.run_until_complete(__clean())
        except asyncio.CancelledError as err:
            MQTTMockClient._logger.debug("Catch the exception!")

    @asyncio.coroutine
    def deliver(self, client):
        try:
            while self._status:
                message = yield from client.deliver_message()
                yield from asyncio.sleep(self._period)
                MQTTMockClient._logger.info("Message: %s" % message.data)
        except ClientException as ce:
            MQTTMockClient._logger.error("Client exception: %s" % ce)

    @asyncio.coroutine
    def send(self, client):
        # for i in range(1, 20):
        while self._status:
            time, string = self.device.get()
            print(string)
            yield from client.publish(TOPIC, string.encode('utf-8'), qos=HBMQTT_CONST.QOS_1)
            yield from asyncio.sleep(time)
            MQTTMockClient._logger.debug("Message published")

    @classmethod
    def my_handler(self):
        MQTTMockClient._logger.debug("Trying to cancel...")
        self._status = False
        for task in asyncio.Task.all_tasks():
            task.cancel()
        if len(asyncio.Task.all_tasks()) > 0:
            os.kill(os.getpid(), signal.SIGINT)


def main():
    args = client_parser(sys.argv)
    MAX_VERBOSITY = 5

    verbosity_level = logging.WARNING
    if args.v == 3:
        verbosity_level = logging.NOTSET
    elif args.v == 2:
        verbosity_level = logging.DEBUG
    elif args.v == 1:
        verbosity_level = logging.INFO
    elif args.v == 0:
        verbosity_level = logging.CRITICAL

    LOGGER_NAME = "MQTT_Generator"

    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=verbosity_level, format=formatter)
    logger = logging.getLogger(LOGGER_NAME)

    logger.handlers = []
    if args.q or args.v == 0:
        logger.addHandler(logging.NullHandler())
    elif args.log_file:
        file_handler = logging.FileHandler(args.log_file)
        logger.addHandler(file_handler)
    else:
        logger.addHandler(logging.StreamHandler())

    # NP: Cloud Nothings — Cut You
    # I need something I can hurt

    client = MQTTMockClient(args.port, args.period)
    client.setup()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, client.my_handler)

    # loop.run_until_complete(clean(client))
    try:
        client.run()
    finally:
        client.clean()
        loop.close()

if __name__ == '__main__':
    main()