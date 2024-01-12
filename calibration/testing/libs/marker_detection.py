#!/usr/bin/env python

import cv2
import numpy as np
import cv2.aruco as aruco
from frameCorrection import get_warped_frame


def detect_markers(url, boundary_ids, aruco_dictionary):
    cap = cv2.VideoCapture(url)

    # Create ArUco parameters
    parameters = cv2.aruco.DetectorParameters()

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        warped_frame, marker_corners_dict = get_warped_frame(frame, boundary_ids, 10)

        if warped_frame is not None:
            # Detect markers within the warped frame
            corners, ids, _ = cv2.aruco.detectMarkers(
                warped_frame, aruco_dictionary, parameters=parameters
            )

            # Draw markers on the warped frame
            if ids is not None:
                for i in range(len(ids)):
                    image = aruco.drawDetectedMarkers(warped_frame, corners, ids)

                    # Extract marker positions
                    marker_positions = {}
                    for i, marker_id in enumerate(ids):
                        marker_positions[marker_id[0]] = corners[i][0]

                    return marker_positions

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def find_nearest_marker_from_bot(
    marker_positions, bot_id, boundary_ids, red_area, green_area
):
    marker_bot = np.array(marker_positions[bot_id])
    distances = {}
    for marker_id, position in marker_positions.items():
        if (
            marker_id != bot_id
            and marker_id != green_area
            and marker_id != red_area
            and marker_id not in boundary_ids
        ):
            marker_position = np.array(position)
            distance = np.linalg.norm(marker_position - marker_bot)
            distances[marker_id] = distance

    if len(distances) > 0:
        nearest_marker = min(distances, key=distances.get)
    else:
        return None

    obstacle_markers = [
        marker_id
        for marker_id in marker_positions.keys()
        if marker_id not in boundary_ids
        and marker_id != red_area
        and marker_id != green_area
        and marker_id != nearest_marker
        and marker_id != bot_id
    ]
    return nearest_marker, obstacle_markers
