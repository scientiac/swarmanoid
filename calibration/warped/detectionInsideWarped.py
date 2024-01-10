#!/usr/bin/env python

import cv2
import numpy as np
import cv2.aruco as aruco


def get_warped_frame(input_frame, marker_ids):
    # Load camera parameters from YAML file
    fs = cv2.FileStorage("miatoll.yml", cv2.FILE_STORAGE_READ)
    camera_matrix = fs.getNode("new_matrix").mat()
    dist_coefficients = fs.getNode("distortion_coef").mat()
    fs.release()

    # Detect markers in the frame
    corners, ids, _ = cv2.aruco.detectMarkers(
        input_frame, aruco_dict, parameters=parameters
    )

    marker_corners_dict = {marker_id: None for marker_id in marker_ids}

    if ids is not None:
        # Extract corners of the specified markers
        for marker_id in marker_ids:
            index = np.where(ids == marker_id)
            if len(index[0]) > 0:
                marker_corners_dict[marker_id] = corners[index[0][0]][0]

    # Check if all specified markers are detected
    if all(value is not None for value in marker_corners_dict.values()):
        # Get the width and height of the frame
        frame_width, frame_height = input_frame.shape[1], input_frame.shape[0]

        # Define the corners of the big marker
        big_marker_corners = [
            marker_corners_dict[marker_ids[3]][2],  # TL = 0
            marker_corners_dict[marker_ids[1]][1],  # BL = 3
            marker_corners_dict[marker_ids[0]][0],  # BR = 2
            marker_corners_dict[marker_ids[2]][3],  # TR = 1
        ]

        # Calculate perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(
            np.float32(big_marker_corners),
            np.float32(
                [
                    [frame_width, frame_height],
                    [frame_width, 0],
                    [0, 0],
                    [0, frame_height],
                ]
            ),
        )

        # Warp the frame using the perspective transformation matrix
        warped_frame = cv2.warpPerspective(
            input_frame, matrix, (frame_width, frame_height)
        )

        return warped_frame, marker_corners_dict

    return None, None  # Return None if not all markers are detected


# Example usage:
url = "http://127.0.0.1:5000/video_feed"
cap = cv2.VideoCapture(url)

marker_ids = [1, 2, 4, 3]  # Specify the ArUco marker IDs

# Define the dictionary to use
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Create ArUco parameters
parameters = cv2.aruco.DetectorParameters()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    warped_frame, marker_corners_dict = get_warped_frame(frame, marker_ids)

    if warped_frame is not None:
        # Detect markers within the warped frame
        corners, ids, _ = cv2.aruco.detectMarkers(
            warped_frame, aruco_dict, parameters=parameters
        )

        # Draw markers on the warped frame
        if ids is not None:
            for i in range(len(ids)):
                # Draw a rectangle around the detected marker
                cv2.polylines(
                    warped_frame, [np.int32(corners[i])], True, (0, 255, 0), 2
                )

        # Display the result
        cv2.imshow("Detected Markers in Warped Frame", warped_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
