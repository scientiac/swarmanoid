import machine
from umqtt.simple import MQTTClient

# MQTT configuration
client_id = "teserrabot"
broker_address = "192.168.35.190"
led_topic = b"led2"

# LED Pin
led_pin = machine.Pin(15, machine.Pin.OUT)


# On/Off logic
def callback(topic, msg):
    print(f"Received message on topic {topic.decode('utf-8')}: {msg.decode('utf-8')}")

    if topic == led_topic:
        if msg == b"on":
            print("Turning on the LED")
            # Turn on the LED
            led_pin.on()
        elif msg == b"off":
            print("Turning off the LED")
            # Turn off the LED
            led_pin.off()


c = MQTTClient(client_id, broker_address)
c.set_callback(callback)
c.connect()
c.subscribe(led_topic)

print("Waiting for messages...")
while True:
    c.wait_msg()
