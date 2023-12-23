#!/usr/bin/env python

import sys
import subprocess


def run_aruco():
    # Specify the path to single_aruco.py
    aruco = "./src/aruco.py"
    subprocess.run(["python", aruco])


def run_mqtt():
    # Specify the path to multi_aruco.py
    mqtt = "./src/mqtt.py"
    subprocess.run(["python", mqtt])


def main():
    if len(sys.argv) == 1:
        # Run single_aruco.py for the default case
        run_aruco()
    elif len(sys.argv) == 2 and (sys.argv[1] == "--mqtt" or sys.argv[1] == "-m"):
        # Run multi_aruco.py for the --multiple or -m option
        run_mqtt()
    else:
        print("Invalid command. Usage: ./main.py [--mqtt|-m]")


if __name__ == "__main__":
    main()
