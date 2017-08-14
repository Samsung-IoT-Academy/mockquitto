import sys
import os
import signal
import asyncio
import logging
import gettext

gettext.install('mockquitto', 'locale', ['ngettext'])

from hbmqtt.client import MQTTClient, ClientException, ConnectException
import hbmqtt.mqtt.constants as HBMQTT_CONST

from mockquitto.client.cli_utils import client_parser
from mockquitto.utils.prettify import json_prettifier
from mockquitto.client.devices.factories import IoTAcademyFactory

class MQTTMockClient:
    _logger = None
    _logger_send = None
    _logger_send_attrs = {
        'format': "sss",
        'handler': logging.NullHandler()
    }

    def __init__(self, port, period=1, logger_name="mockquitto.client.MQTTMockClient", loop=None, status=True,
                 parent_logger: logging.Logger = None, *, sub_topic: str = 'devices/lora/807B85902000019A/gps'):
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._status = status
        self._client = MQTTClient()
        self._broker_port = port
        self._subsribe_topic = sub_topic
        self._period = period

        self._devices = []
        self._coros = []
        if __class__._logger is None:
            if parent_logger is None:
                __class__._logger = logging.getLogger(logger_name)
            else:
                __class__._logger = parent_logger.getChild(str(self.__class__))
            __class__._logger_send = __class__._logger.getChild("coro.sender")


    @property
    def client(self):
        return self._client

    @property
    def event_loop(self):
        return self._loop

    @classmethod
    def get_logger(cls):
        return cls._logger

    def setup(self, cases=None):
        @asyncio.coroutine
        def __internal_setup():
            try:
                yield from self._client.connect("mqtt://localhost:" + str(self._broker_port))
                print(_("Connected to port {port:d}").format(port=self._broker_port))
            except ConnectException:
                MQTTMockClient._logger.critical("Cannot connect to broker. Exit...")
                exit(0)
            except OSError:
                pass

            yield from self._client.subscribe([
                (self._subsribe_topic, HBMQTT_CONST.QOS_1),
            ])

        if isinstance(cases, (list, tuple)):
            while cases:
                case = cases.pop(0)
                if case == 1:
                    self._devices.append(IoTAcademyFactory.create_temp_hum())
                elif case == 5:
                    for e in IoTAcademyFactory.create_luminocity(), IoTAcademyFactory.create_adc():
                        self._devices.append(e)
        else:
            self._devices.append(IoTAcademyFactory.create_temp_hum())

        self._coros = [self.create_coro(d) for d in self._devices]

        try:
            self._loop.run_until_complete(__internal_setup())
        except asyncio.CancelledError:
            pass

        return self._client

    def run(self):
        try:
            self.task_deliver = self._loop.create_task(self.deliver(self._client))
            self.tasks_send = [asyncio.ensure_future(c(), loop=self._loop) for c in self._coros]
            self._loop.run_forever()
        except asyncio.CancelledError as err:
            pass

    def stop(self):
        while self.task_deliver.cancelled is False and not all(t.cancelled for t in self.tasks_send):
            self.task_deliver.cancel()
            for t in self.tasks_send:
                t.cancel()


    def clean(self):
        @asyncio.coroutine
        def __clean():
            yield from self._client.unsubscribe([self._subsribe_topic])
            yield from self._client.disconnect()
            yield from asyncio.sleep(0.5)

        try:
            self._loop.run_until_complete(__clean())
        except asyncio.CancelledError as err:
            pass

    @asyncio.coroutine
    def deliver(self, client):
        try:
            while self._status:
                message = yield from client.deliver_message()
                yield from asyncio.sleep(self._period)
                MQTTMockClient._logger.info("Message: {}".format(message.data))
        except ClientException as ce:
            MQTTMockClient._logger.error("Client exception: {}".format(ce))

    def create_coro(self, device):
        @asyncio.coroutine
        def send(device=device, self=self, client=self._client):
            while self._status:
                time, string = device.get()
                MQTTMockClient.get_logger().debug(json_prettifier(string))
                yield from client.publish(device.mqtt_topic, string.encode('utf-8'), qos=HBMQTT_CONST.QOS_1)
                yield from asyncio.sleep(time)
                MQTTMockClient.get_logger().debug("Message published")
        return send

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
    root_logger = logging.getLogger()
    logger = logging.getLogger('mockquitto.client')
    logger.handlers = []
    verbosity_level = logging.NOTSET

    verbosity = args.v - args.q
    if verbosity == 3:
        verbosity_level = logging.DEBUG
    elif verbosity == 2:
        verbosity_level = logging.INFO
    elif verbosity == 1:
        verbosity_level = logging.WARNING
    elif verbosity == 0:
        verbosity_level = logging.ERROR
    elif verbosity == -1:
        verbosity_level = logging.CRITICAL
    elif verbosity == -2:
        verbosity_level = logging.CRITICAL
        logger.addHandler(logging.NullHandler())
        root_logger.addHandler(logging.NullHandler())

    if verbosity in [0, -1, -2]:
        root_logger.setLevel(verbosity_level)

    formatter = logging.Formatter(fmt="[%(asctime)s] :: %(levelname)s :: %(message)s")
    logger.setLevel(verbosity_level)

    if not logger.hasHandlers():
        if args.log_file:
            file_handler = logging.FileHandler(args.log_file)
            logger.addHandler(file_handler)
        else:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

    client = MQTTMockClient(args.port, args.period, parent_logger=logger)
    client.setup(args.case)
    # loop.add_signal_handler(signal.SIGINT, client.my_handler)

    # loop.run_until_complete(clean(client))
    try:
        logger.debug("Run the client")
        client.run()
    except KeyboardInterrupt:
        MQTTMockClient._logger.critical("Interrupted by user. Exit...")
        client.stop()
    finally:
        client.clean()
        client.event_loop.close()

if __name__ == '__main__':
    main()