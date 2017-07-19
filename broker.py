#! /usr/bin/env python

import logging
import asyncio
import signal

from hbmqtt.broker import Broker

def stop_broker_handler(broker, loop):
    loop.run_until_complete(broker.shutdown())
    loop.stop()
    loop.close()
    exit(0)


async def broker_coro(broker):
    await broker.start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)


    config = {
        'listeners': {
            'default': {
                'type': 'tcp',
                'bind': 'localhost:1884',
                'max_connections': 10,
            }
        },
        'sys_interval': 10,
    }
    broker = Broker(config)

    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, stop_broker_handler, broker, loop)
    loop.run_until_complete(broker_coro(broker))
    loop.run_forever()
