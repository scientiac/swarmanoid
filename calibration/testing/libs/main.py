#!/usr/bin/env python

import cv2.aruco as aruco
from marker_detection import detect_markers, find_nearest_marker_from_bot

url = "http://127.0.0.1:5000/video_feed"  # Replace with your video feed URL

# Boundary IDs
markerTL = 1
markerTR = 2
markerBL = 4
markerBR = 3

# Define the boundary markers and their positions
boundary_ids = [markerTL, markerTR, markerBL, markerBR]

# Define the dictionary to use
aruco_dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Define bot's ID
bot_id = 69
red_area = 33
green_area = 22


def main():
    # Example usage:
    marker_positions = detect_markers(url, boundary_ids, aruco_dictionary)

    chosen_marker, avoided_waste_markers = find_nearest_marker_from_bot(
        marker_positions, bot_id, boundary_ids, red_area, green_area
    )

    # Process the detected marker positions as needed
    # for marker_id, marker_position in marker_positions.items():
    #     print(f"Marker ID: {marker_id}, Position: {marker_position}")

    print(chosen_marker)
    print(avoided_waste_markers)

    # Continue with the rest of your program logic


if __name__ == "__main__":
    main()
