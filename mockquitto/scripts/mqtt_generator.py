import paho.mqtt.client as mqttc
import time
import random

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.user_data_set("ы" * random.randint(1, 5))
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def on_publish_custom(client, userdata, mid):
    print("--- M E S S A G E ---\n\ttopic: {}\n\t msg: {}\n\t ыыы: {}".\
        format("paho/temperature", temperature, userdata))

def main():
    client = mqttc.Client(userdata="ОЙ")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish_custom

    client.connect("localhost", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_start()

    while True:
        time.sleep(5)
        temperature = random.randint(0, 273)
        client.publish("paho/temperature", payload=temperature)

if __name__=='__main__':
    main()