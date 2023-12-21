import paho.mqtt.publish as publish
import time

broker_address = "192.168.35.190"
led_topic = "led"
led_topic2 = "led2"

while True:
    # Turn on the LED on the ESP8266
    publish.single(led_topic, "onn", hostname=broker_address)
    publish.single(led_topic2, "on", hostname=broker_address)

    time.sleep(1)  # Wait for a moment

    # Turn off the LED on the ESP8266
    publish.single(led_topic, "offf", hostname=broker_address)
    publish.single(led_topic2, "off", hostname=broker_address)

    time.sleep(1)  # Wait for a moment
