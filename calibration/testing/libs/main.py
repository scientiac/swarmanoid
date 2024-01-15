#!/usr/bin/env python

import cv2.aruco as aruco
from marker_detection import (
    detect_markers,
    find_nearest_marker_from_bot,
    getMarkerPosition,
    calculateDistances,
)
from astar import find_path

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

GRID_SIZE = 1000

def main():
    # Example usage:
    marker_positions = detect_markers(url, boundary_ids, aruco_dictionary)

    chosen_marker, avoided_waste_markers = find_nearest_marker_from_bot(
        marker_positions, bot_id, boundary_ids, red_area, green_area
    )

    center, left_corner, right_corner = getMarkerPosition(
        bot_id, boundary_ids, aruco_dictionary, url
    )

    def followPathWithArUco(bot_id, path):
        # Check if path is iterable (a list, for example)
        if not isinstance(path, (list, tuple)):
            raise ValueError("Path should be an iterable (list, tuple, etc.)")

        for point in path:
            marker_position = getMarkerPosition(
                bot_id, boundary_ids, aruco_dictionary, url
            )

            if marker_position is not None:
                center, left_corner, right_corner = marker_position
                right_distance, left_distance, center_distance = calculateDistances(
                    center, point
                )

                center_tuple = tuple(center)
                left_corner_tuple = tuple(left_corner)
                right_corner_tuple = tuple(right_corner)

                print(center_tuple, left_corner_tuple, right_corner_tuple)

                # moveTowardsGoal(right_distance, left_distance, center_distance, t)

    # Process the detected marker positions as needed
    # for marker_id, marker_position in marker_positions.items():
    #     print(f"Marker ID: {marker_id}, Position: {marker_position}")

    path = find_path(
        GRID_SIZE,
        marker_positions,
        chosen_marker,
        avoided_waste_markers,
        url,
        bot_id,
    )

    followPathWithArUco(bot_id, path)

    print(chosen_marker)
    print(avoided_waste_markers)

    center_tuple = tuple(center)
    left_corner_tuple = tuple(left_corner)
    right_corner_tuple = tuple(right_corner)

    print(center_tuple)
    print(left_corner_tuple, right_corner_tuple)

    # Continue with the rest of your program logic


if __name__ == "__main__":
    main()
