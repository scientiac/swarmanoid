#!/usr/bin/env bash

echo "Are you in the project's root directory? (y/n)"
read in_root_dir

if [ "$in_root_dir" != "y" ]; then
	echo "Exiting script as you are not in the project's root directory."
	exit 1
fi

echo "Is the ESP device plugged in? (y/n)"
read esp_plugged_in

if [ "$esp_plugged_in" != "y" ]; then
	echo "Exiting script as the ESP device is not plugged in."
	exit 1
fi

echo "Enter the new MQTT broker address:"
read new_broker_address

# Update broker address in mqtt.py
sed -i "s/broker_address = \"[^\"]*\"/broker_address = \"$new_broker_address\"/" ./micropython/mqtt.py
sed -i "s/broker_address = \"[^\"]*\"/broker_address = \"$new_broker_address\"/" ./src/mqtt_server.py
sed -i "s/broker_address = \"[^\"]*\"/broker_address = \"$new_broker_address\"/" ./src/single_aruco.py

echo "Do you want to change Wi-Fi credentials? (y/n)"
read change_wifi_credentials

if [ "$change_wifi_credentials" = "y" ]; then
	echo "Enter the new Wi-Fi SSID:"
	read new_wifi_ssid

	echo "Enter the new Wi-Fi password:"
	read new_wifi_password

	# Update Wi-Fi credentials in boot.py
	sed -i "s/ssid = \"[^\"]*\"/ssid = \"$new_wifi_ssid\"/" ./micropython/boot.py
	sed -i "s/password = \"[^\"]*\"/password = \"$new_wifi_password\"/" ./micropython/boot.py
fi

echo "Changes applied successfully."

echo "Do you want to push the updated code to the ESP device? (y/n)"
read push_to_esp

if [ "$push_to_esp" = "y" ]; then
	# Push updated code using ampy
	ampy -p /dev/ttyUSB0 put ./micropython/boot.py
	ampy -p /dev/ttyUSB0 put ./micropython/mqtt.py
	echo "Code pushed to ESP device."
else
	echo "Code not pushed to ESP device. You can manually upload the files using ampy."
fi
