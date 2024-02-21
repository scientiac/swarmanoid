# Setting up esp8266 for micropython
> no need if youre using regular .ino code

Using esptool.py you can erase the flash with the command:
```
esptool.py --port /dev/ttyUSB0 erase_flash
```
And then deploy the new [firmware](https://micropython.org/download/ESP8266_GENERIC/) using:
```
# the following command flashes the firmware that I am using from the `etc` directory in of my repo.
# you might want to flash the latest firmware by downloading it from the link given above.
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ./etc/ESP8266_GENERIC-20231005-v1.21.0.bin
```

```
# if you cant access the repl even after sucessfully flashing the firmware
esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect --flash_mode dout 0 ./etc/ESP8266_GENERIC-20231005-v1.21.0.bin
```

## Connecting to the USB serial repl
```
screen /dev/ttyUSB0 115200
```

> Also checkout [CHEATSHEET](src/micropython/CHEATSHEET.md) for setting up essentials like wifi.

You can also make use of the [webrepl](https://learn.adafruit.com/micropython-basics-esp8266-webrepl/access-webrepl) which is also the primary way of sending files to the client.

To enable the webrepl just `import webrepl_setup` in the serial repl and you're good to go.


