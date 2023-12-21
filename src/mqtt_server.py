import paho.mqtt.publish as publish
import time

broker_address = "192.168.1.80"
led_topic = "led"

while True:
    # Turn on the LED on the ESP8266
    publish.single(led_topic, "on", hostname=broker_address)

    time.sleep(1)  # Wait for a moment

    # Turn off the LED on the ESP8266
    publish.single(led_topic, "off", hostname=broker_address)

    time.sleep(1)  # Wait for a moment
