import machine
from umqtt.simple import MQTTClient
import time
from secrets import BROKER_ADDRESS

# MQTT configuration
client_id = "teserraclient"
broker_address = BROKER_ADDRESS
led_topic = b"led"
bot_topic = b"led"

# LED Pin
led_pin = machine.Pin(15, machine.Pin.OUT)

# Bot config
Lmotor1 = machine.Pin(5, machine.Pin.OUT)
Lmotor2 = machine.Pin(4, machine.Pin.OUT)

Rmotor1 = machine.Pin(0, machine.Pin.OUT)
Rmotor2 = machine.Pin(14, machine.Pin.OUT)


def forward():
    Lmotor1.on()
    Lmotor2.off()
    Rmotor1.on()
    Rmotor2.off()


def back():
    Lmotor1.off()
    Lmotor2.on()
    Rmotor1.off()
    Rmotor2.on()


def left():
    Lmotor1.off()
    Lmotor2.on()
    Rmotor1.on()
    Rmotor2.off()
    time.sleep_ms(100)
    stop()


def right():
    Lmotor1.on()
    Lmotor2.off()
    Rmotor1.off()
    Rmotor2.on()
    time.sleep_ms(100)
    stop()


def stop():
    Lmotor1.off()
    Lmotor2.off()
    Rmotor1.off()
    Rmotor2.off()


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
        if msg == b"front":
            forward()
            print("Front")
        elif msg == b"back":
            print("Back")
            back()
        elif msg == b"left":
            print("Left")
            left()
        elif msg == b"right":
            print("Right")
            right()
        elif msg == b"stop":
            print("Stop")
            stop()


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
