import paho.mqtt.client as mqtt
from micropython.secrets import BROKER_ADDRESS
import time

broker_address = BROKER_ADDRESS
led_topic = "led"
led_topic2 = "led2"
client_id = "python"


# Define callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed with code", rc)


def on_disconnect(client, userdata, rc):
    print("Disconnected from broker")


# Create an MQTT client
client = mqtt.Client(client_id=client_id)

# Set callback functions
client.on_connect = on_connect
client.on_disconnect = on_disconnect

# Connect to the broker
client.connect(broker_address, 1883, 60)

try:
    while True:
        # Turn on the LED on the ESP8266
        client.publish(led_topic, "on")
        client.publish(led_topic2, "on")

        time.sleep(1)  # Wait for a moment

        # Turn off the LED on the ESP8266
        client.publish(led_topic, "off")
        client.publish(led_topic2, "off")

        time.sleep(1)  # Wait for a moment

except KeyboardInterrupt:
    # Gracefully exit the script
    client.disconnect()
