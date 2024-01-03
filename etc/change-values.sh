#!/usr/bin/env bash

ssid=""
ip_address=""
password=""

# Function to prompt yes/no questions with default value 'N'
prompt_yes_no() {
  local question=$1
  local default_value=${2:-N} # Default value is 'N'
  local user_input

  read -p "$question (y/n) [$default_value]: " user_input

  # Convert to lowercase and use default if input is empty
  user_input=$(echo "$user_input" | tr '[:upper:]' '[:lower:]')
  user_input=${user_input:-$default_value}

  echo "$user_input"
}

# Function to prompt for user input
prompt_input() {
  local question=$1
  local user_input

  read -p "$question: " user_input
  echo "$user_input"
}

# Function to detect Wi-Fi information
detect_wifi_info() {
  # Detect Wi-Fi interface dynamically
  local wifi_interface
  if [ "$(command -v iwconfig)" ]; then
    wifi_interface=$(iwconfig 2>/dev/null | grep -oP "^[^\s]+")
  elif [ "$(command -v ip)" ]; then
    wifi_interface=$(ip link show | grep -oP "^\d+:\s+\K\w+(?=@)")
  fi

  if [ -n "$wifi_interface" ]; then
    # Retrieve Wi-Fi SSID
    if [ "$(command -v nmcli)" ]; then
      ssid=$(nmcli -t -f active,ssid dev wifi | grep '^yes' | cut -d: -f2)
    elif [ "$(command -v iwgetid)" ]; then
      ssid=$(iwgetid -r)
    fi

    # Retrieve Wi-Fi password using nmcli
    if [ "$(command -v nmcli)" ]; then
      password=$(nmcli device wifi show-password | grep "Password" | awk '{print $2}')
    fi

    # Retrieve Wi-Fi IP address
    if [ "$(command -v ip)" ]; then
      ip_address=$(ip addr show "$wifi_interface" | awk '/inet /{print $2}' | cut -d'/' -f1)
    elif [ "$(command -v ifconfig)" ]; then
      ip_address=$(ifconfig "$wifi_interface" | awk '/inet /{print $2}' | cut -d':' -f2)
    fi
  fi

  echo "Wi-Fi SSID: $ssid"
  echo "Wi-Fi Password: $password"
  echo "IP Address: $ip_address"
}

# Check if the system is macOS
is_macos=$(uname -s)
if [ "$is_macos" != "Darwin" ]; then
  # Automatically detect Wi-Fi information
  echo "Detecting Wi-Fi information automatically..."
  detect_wifi_info

  # Ask for confirmation
  confirm_auto_detection=$(prompt_yes_no "Is the detected information correct?")

  if [ "$confirm_auto_detection" = "y" ]; then
    sed -i "s/BROKER_ADDRESS = \"[^\"]*\"/BROKER_ADDRESS = \"$ip_address\"/" ./src/micropython/secrets.py
    sed -i "s/WIFI_SSID = \"[^\"]*\"/WIFI_SSID = \"$ssid\"/" ./src/micropython/secrets.py
    sed -i "s/WIFI_PASSWORD = \"[^\"]*\"/WIFI_PASSWORD = \"$password\"/" ./src/micropython/secrets.py

    echo "Changes applied successfully."
  else
    echo "Automatic detection unsuccessful. Please set values manually."

    # Update values in secrets.py
    new_broker_address=$(prompt_input "Enter the new MQTT broker address")
    new_wifi_ssid=$(prompt_input "Enter the new Wi-Fi SSID")
    new_wifi_password=$(prompt_input "Enter the new Wi-Fi password")

    sed -i "s/BROKER_ADDRESS = \"[^\"]*\"/BROKER_ADDRESS = \"$new_broker_address\"/" ./src/micropython/secrets.py
    sed -i "s/WIFI_SSID = \"[^\"]*\"/WIFI_SSID = \"$new_wifi_ssid\"/" ./src/micropython/secrets.py
    sed -i "s/WIFI_PASSWORD = \"[^\"]*\"/WIFI_PASSWORD = \"$new_wifi_password\"/" ./src/micropython/secrets.py

    echo "Changes applied successfully."
  fi
else
  echo "Automatic detection is not supported on macOS. Please set values manually."

  # Update values in secrets.py
  new_broker_address=$(prompt_input "Enter the new MQTT broker address")
  new_wifi_ssid=$(prompt_input "Enter the new Wi-Fi SSID")
  new_wifi_password=$(prompt_input "Enter the new Wi-Fi password")

  sed -i "s/BROKER_ADDRESS = \"[^\"]*\"/BROKER_ADDRESS = \"$new_broker_address\"/" ./src/micropython/secrets.py
  sed -i "s/WIFI_SSID = \"[^\"]*\"/WIFI_SSID = \"$new_wifi_ssid\"/" ./src/micropython/secrets.py
  sed -i "s/WIFI_PASSWORD = \"[^\"]*\"/WIFI_PASSWORD = \"$new_wifi_password\"/" ./src/micropython/secrets.py

  echo "Changes applied successfully."
fi

# Ask if the changes are to be pushed
push_to_device=$(prompt_yes_no "Do you want to update it to esp? (Make sure it's plugged in!)")

if [ "$push_to_device" == "y" ]; then
  echo "Pushing the values to esp..."
  ampy -p /dev/ttyUSB0 put ./src/micropython/secrets.py
  echo "You can now disconnect and reconnect the esp."
else
  echo "Exiting script..."
  exit 1
fi
