import sys
import signal
import logging
import functools
import asyncio

from hbmqtt.broker import Broker

from mockquitto.broker import BrokerConfig

@asyncio.coroutine
def broker_coro(broker, config):
    yield from broker.start()


def main(*args, **kwargs):
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    logger = logging.getLogger(name="MQTT-Broker")

    config = BrokerConfig()
    broker = Broker(config.get_config())

    logger.info("Listening {} on port {}".format(config.domain, config.port))

    loop = asyncio.get_event_loop()

    loop.run_until_complete(broker_coro(broker, config))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(broker.shutdown())
    finally:
        logger.info("Closing")
        loop.close()

if __name__ == '__main__':
    main(sys.argv)