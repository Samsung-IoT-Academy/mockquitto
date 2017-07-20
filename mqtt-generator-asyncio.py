#! /usr/bin/env python

import os
import signal
import asyncio
import argparse
import logging

from hbmqtt.client import MQTTClient, ClientException, ConnectException
import hbmqtt.mqtt.constants as HBMQTT_CONST

TOPIC = 'paho/temperature'


class MQTTMockClient:

    _logger = None

    def __init__(self, port, logger_name="MQTT_Generator", loop=None, status=True):
        self._loop = asyncio.get_event_loop() if (loop is None) else loop
        self._status = status
        self._client = MQTTClient()
        self._broker_port = port
        if MQTTMockClient._logger is None:
            MQTTMockClient._logger = logging.getLogger(logger_name)

    @property
    def client(self):
        return self._client

    def setup(self):
        async def __internal_setup():
            try:
                await self._client.connect("mqtt://localhost:" + str(self._broker_port))
            except ConnectException:
                MQTTMockClient._logger.critical("Cannot connect to broker. Exit...")
                exit(0)

            await self._client.subscribe([
                (TOPIC, HBMQTT_CONST.QOS_1),
            ])

        self._loop.run_until_complete(__internal_setup())
        return self._client

    def run(self):
        async def __main():
            task_deliver = self._loop.create_task(self.deliver(self._client))
            task_send = self._loop.create_task(self.send(self._client))
            await task_deliver
            await task_send

        try:
            self._loop.run_until_complete(__main())
        except asyncio.CancelledError as err:
            MQTTMockClient._logger.debug("Catch the exception!")

    def clean(self):
        async def __clean():
            await self._client.unsubscribe([TOPIC])
            await self._client.disconnect()
        try:
            self._loop.run_until_complete(__clean())
        except asyncio.CancelledError as err:
            MQTTMockClient._logger.debug("Catch the exception!")

    async def deliver(self, client):
        try:
            while self._status:
                message = await client.deliver_message()
                await asyncio.sleep(1)
        except ClientException as ce:
            MQTTMockClient._logger.error("Client exception: %s" % ce)

    async def send(self, client):
        # for i in range(1, 20):
        while self._status:
            message = await client.publish(TOPIC, b'i want to publish', qos=HBMQTT_CONST.QOS_1)
            await asyncio.sleep(1)
            MQTTMockClient._logger.debug("Message published")

    @classmethod
    def my_handler(self):
        MQTTMockClient._logger.debug("Trying to cancel...")
        self._status = False
        for task in asyncio.Task.all_tasks():
            task.cancel()
        if len(asyncio.Task.all_tasks()) > 0:
            os.kill(os.getpid(), signal.SIGINT)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Example daemon in Python")
    parser.add_argument('-p', '--port', help="Broker's port to connect", action="store", default=1883)
    parser.add_argument('-v', help='Verbose output', action="count", default=0)
    parser.add_argument('-q', help="Don't output anything", action="store_true")
    parser.add_argument('--log_file', nargs='?', help='File for logging', action="store", const="log.log",
                        default=None)
    parser.set_defaults(v=0, log_to_file=None)
    args = parser.parse_args()

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
    if args.q:
        logger.addHandler(logging.NullHandler())
    elif args.log_file:
        file_handler = logging.FileHandler("{}".format(args.log_file))
        logger.addHandler(file_handler)
    else:
        logger.addHandler(logging.StreamHandler())

    client = MQTTMockClient(args.port)
    client.setup()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, client.my_handler)

    # loop.run_until_complete(clean(client))
    try:
        client.run()
    finally:
        client.clean()
        loop.close()