#! /usr/bin/env python

from sys import stderr
import logging
import asyncio
import signal

from hbmqtt.client import MQTTClient, ClientException
import hbmqtt.mqtt.constants as HBMQTT_CONST

logger = logging.getLogger(__name__)
TOPIC = 'paho/temperature'

def my_handler(loop):
    print("Trying to cancelize...")
    for task in asyncio.Task.all_tasks():
        task.cancel()

async def deliver(client):
    try:
        while True:
            print("Delivering...", file=stderr)
            message = await client.deliver_message()
            print("%d:  %s => %s" % (2, message.topic, str(message.data)))
            await asyncio.sleep(1)
    except ClientException as ce:
        logger.error("Client exception: %s" % ce)

async def send(client):
    # for i in range(1, 20):
    while True:
        print("Sending...", file=stderr)
        message = await client.publish(TOPIC, b'i want to publish', qos=HBMQTT_CONST.QOS_1)
        print("%d:  %s => %s" % (1, message.topic, str(message.data)), file=stderr)
        await asyncio.sleep(1)
        logger.info("Message published")

async def subscribe_topic(client):
    print("Subscribing...", file=stderr)
    await client.subscribe([
            (TOPIC, HBMQTT_CONST.QOS_1),
         ])

async def main(loop, client):
    task_deliver = loop.create_task(deliver(client))
    task_send = loop.create_task(send(client))
    await task_deliver
    await task_send

async def setup():
    client = MQTTClient()
    print("Connecting...", file=stderr)
    await client.connect("mqtt://localhost:1883")
    await subscribe_topic(client)
    return client

async def clean(client):
    print("Unsubscribing and disconnecting...")
    await client.unsubscribe([TOPIC])
    await client.disconnect()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(setup())
    loop.add_signal_handler(signal.SIGINT, my_handler, loop)
    # loop.run_until_complete(main(loop, client))
    # loop.run_until_complete(clean(client))
    try:
        loop.run_until_complete(main(loop, client))
    except asyncio.CancelledError:
        loop.run_until_complete(clean(client))
    finally:
        loop.close()