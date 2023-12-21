import esp
import os, machine
import gc
import webrepl

webrepl.start()
gc.collect()

import network
import time
import machine

# Wi-Fi configuration
ssid = "scientiac"
password = "hehehehe"


# Function to connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(ssid, password)
        # wlan.connect(ssid)

        while not wlan.isconnected():
            time.sleep(1)

    print("Connected to WiFi")


# Connect to Wi-Fi
connect_wifi()

# Check if Wi-Fi connection is successful before executing mqtt.py
if network.WLAN(network.STA_IF).isconnected():
    # Execute mqtt.py
    try:
        # import mqtt2  # Replace 'mqtt' with the actual name of your Python script

        import mqtt  # Replace 'mqtt' with the actual name of your Python script
    except Exception as e:
        print("Error executing mqtt.py:", e)
