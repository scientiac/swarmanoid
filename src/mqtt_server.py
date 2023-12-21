import paho.mqtt.publish as publish
import time

broker_address = "192.168.1.80"
led_topic = "led"
led_topic2 = "led2"

while True:
    # Turn on the LED on the ESP8266
    publish.single(led_topic, "on", hostname=broker_address)
    publish.single(led_topic2, "on", hostname=broker_address)

    time.sleep(1)  # Wait for a moment

    # Turn off the LED on the ESP8266
    publish.single(led_topic, "off", hostname=broker_address)
    publish.single(led_topic2, "off", hostname=broker_address)

    time.sleep(1)  # Wait for a moment
