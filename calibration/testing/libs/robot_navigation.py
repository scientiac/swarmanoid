#!/usr/bin/env python

import paho.mqtt.publish as publish
import time

BROKER_ADDRESS = "192.168.1.80"  # Replace with your MQTT broker address
CAR_TOPIC = "wave"  # Replace with the topic your car code is subscribed to


def move_towards_goal(right_distance, left_distance, center_distance, t):
    global speed

    if center_distance < right_distance and center_distance < left_distance:
        print("Backwards!")
        if right_distance > left_distance:
            send_command("down")
            print("back")
        else:
            send_command("up")
            print("front")
    else:
        if right_distance > left_distance and right_distance - left_distance > 3 * t:
            send_command("left")
            print("left")
        elif right_distance > left_distance and right_distance - left_distance > t:
            send_command("left")
            print("left")
        elif left_distance > right_distance and left_distance - right_distance > 3 * t:
            send_command("right")
            print("right")
        elif left_distance > right_distance and left_distance - right_distance > t:
            send_command("right")
            print("right")
        else:
            print("Forwards!")
            send_command("front")


def send_command(command):
    publish.single(CAR_TOPIC, command, hostname=BROKER_ADDRESS)


# Example usage
while True:
    # Simulate distance values (replace with actual sensor readings)
    right_dist = 10
    left_dist = 18
    center_dist = 7
    time.sleep(1)  # Simulate a delay between distance readings
    move_towards_goal(right_dist, left_dist, center_dist, 1)
