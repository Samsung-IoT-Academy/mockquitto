#! /usr/bin/env python

import logging
import asyncio
import os
from hbmqtt.broker import Broker


@asyncio.coroutine
def broker_coro():
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
    yield from broker.start()


if __name__ == '__main__':
    formatter = "[%(asctime)s] :: %(levelname)s :: %(name)s :: %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)
    asyncio.get_event_loop().run_until_complete(broker_coro())
    asyncio.get_event_loop().run_forever()
