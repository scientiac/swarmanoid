#!/bin/bash

# Check if the script is run as root
if [[ $EUID -ne 0 ]]; then
	echo "This script requires root privileges. Please run it with sudo."
	exit 1
fi

# Add the line to the file
echo "experimental-features = nix-command flakes" >>/etc/nix/nix.conf

# Check if the line was added successfully
if grep -q "experimental-features = nix-command flakes" /etc/nix/nix.conf; then
	echo "Successfully added the line to /etc/nix/nix.conf."
	echo "Don't run this script again."
else
	echo "An error occurred while adding the line to /etc/nix/nix.conf."
fi
