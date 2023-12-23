import paho.mqtt.client as mqtt
from micropython.secrets import BROKER_ADDRESS


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed with code", rc)


def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")


def establish_connection():
    client_id = "tesserver"
    client = mqtt.Client(client_id=client_id)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(BROKER_ADDRESS, 1883, 60)

    return client
