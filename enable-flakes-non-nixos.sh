#!/bin/bash

# Set the user's configuration file path
user_nix_conf_file="$HOME/.config/nix/nix.conf"
config_line="experimental-features = nix-command flakes"

# Create the ~/.config/nix/ folder if it doesn't exist
mkdir -p "$(dirname "$user_nix_conf_file")"

# Check if the file exists before reading from it
if [ -f "$user_nix_conf_file" ]; then
	# Check if the line already exists in the user's configuration file
	if grep -q "$config_line" "$user_nix_conf_file"; then
		echo "The line already exists in $user_nix_conf_file. No changes needed."
		exit 0
	fi
fi

# Add the line to the user's configuration file
echo "$config_line" >>"$user_nix_conf_file"

# Check if the line was added successfully
if grep -q "$config_line" "$user_nix_conf_file"; then
	echo "Successfully added the line to $user_nix_conf_file."
	echo "Don't run this script again."
else
	echo "An error occurred while adding the line to $user_nix_conf_file."
	exit 1
fi
