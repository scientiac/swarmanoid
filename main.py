#!/usr/bin/env python

import sys
import subprocess


def run_single_aruco():
    # Specify the path to single_aruco.py
    single_aruco_file = "./src/single_aruco.py"
    subprocess.run(["python", single_aruco_file])


def run_multi_aruco():
    # Specify the path to multi_aruco.py
    multi_aruco_file = "./src/multi_aruco.py"
    subprocess.run(["python", multi_aruco_file])


def main():
    if len(sys.argv) == 1:
        # Run single_aruco.py for the default case
        run_single_aruco()
    elif len(sys.argv) == 2 and (sys.argv[1] == "--multiple" or sys.argv[1] == "-m"):
        # Run multi_aruco.py for the --multiple or -m option
        run_multi_aruco()
    else:
        print("Invalid command. Usage: ./main.py [--multiple|-m]")


if __name__ == "__main__":
    main()
