#!/usr/bin/env python

import sys
import subprocess


def run_aruco():
    # Specify the path to single_aruco.py
    aruco = "./src/aruco.py"
    subprocess.run(["python", aruco])


def run_simulation():
    # Specify the path to multi_aruco.py
    simulation = "./src/simulation.py"
    subprocess.run(["python", simulation])


def main():
    if len(sys.argv) == 1:
        # Run single_aruco.py for the default case
        run_aruco()
    elif len(sys.argv) == 2 and (sys.argv[1] == "--simulate" or sys.argv[1] == "-s"):
        # Run simulation.py for the --simulate or -s option
        run_simulation()
    else:
        print("Invalid command. Usage: ./main.py [--simulate|-s]")

# Main Function
if __name__ == "__main__":
    main()
