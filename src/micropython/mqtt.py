import machine
from umqtt.simple import MQTTClient
import time
from secrets import BROKER_ADDRESS

# MQTT configuration
client_id = "teserraclient"
broker_address = BROKER_ADDRESS
led_topic = b"led"

# LED Pin
led_pin = machine.Pin(15, machine.Pin.OUT)


def connect_mqtt():
    c = MQTTClient(client_id, broker_address)
    c.set_callback(callback)

    while True:
        try:
            c.connect(clean_session=False)
            print("Connected to MQTT broker.")
            c.subscribe(led_topic)
            return c
        except OSError as e:
            print(f"Connection error: {e}")
            print("Retrying in 5 seconds...")
            time.sleep(5)


def callback(topic, msg):
    print(f"Received message on topic {topic.decode('utf-8')}: {msg.decode('utf-8')}")

    if topic == led_topic:
        if msg == b"on":
            print("Turning on the LED")
            led_pin.on()
        elif msg == b"off":
            print("Turning off the LED")
            led_pin.off()


mqtt_client = connect_mqtt()

if mqtt_client:
    print("Waiting for messages...")
    while True:
        try:
            mqtt_client.wait_msg()
        except OSError as e:
            print(f"Error: {e}")
            print("Reconnecting...")
            mqtt_client = connect_mqtt()
            if not mqtt_client:
                break
