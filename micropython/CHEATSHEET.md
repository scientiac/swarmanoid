1. To send files to esp using serial.
```
ampy -p /dev/ttyUSB0 put mqtt.py
```

2. Connecting to the USB serial repl
```
screen /dev/ttyUSB0 115200
```

3. To read all the files from serial.
```
import os

files = os.listdir()
for file in files:
    with open(file, "r") as f:
        content = f.read()
        print(f"File: {file}\nContent: {content}\n")
```

4. To turn on led on 15 GPIO, D8
```
import machine
pin = machine.Pin(15, machine.Pin.OUT)
pin.on()
```
5. To change esp ip wifi ssid and password
```
import network

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="new_ap_ssid", password="new_ap_password")
```
