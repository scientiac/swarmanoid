#!/usr/bin/env python

import cv2
import numpy as np
import cv2.aruco as aruco

# Load camera parameters from YAML file
fs = cv2.FileStorage("miatoll.yml", cv2.FILE_STORAGE_READ)
camera_matrix = fs.getNode("new_matrix").mat()
dist_coefficients = fs.getNode("distortion_coef").mat()
fs.release()

# Define the dictionary to use
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Create ArUco parameters
parameters = cv2.aruco.DetectorParameters()

url = "http://127.0.0.1:5000/video_feed"

# Initialize video capture (use 0 for default camera or provide the video file path)
cap = cv2.VideoCapture(url)  # Change 0 to your camera index or video file path

markerTL = 1
markerTR = 2
markerBL = 4
markerBR = 3

# Define the markers and their positions
marker_ids = [markerTL, markerTR, markerBL, markerBR]
marker_corners_dict = {markerTL: None, markerTR: None, markerBL: None, markerBR: None}

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Detect markers in the frame
    corners, ids, _ = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if ids is not None:
        # Extract corners of the specific markers
        for marker_id in marker_ids:
            index = np.where(ids == marker_id)
            if len(index[0]) > 0:
                marker_corners_dict[marker_id] = corners[index[0][0]][0]

    # Check if all markers are detected
    if all(value is not None for value in marker_corners_dict.values()):
        # Get the width and height of the frame
        frame_width, frame_height = frame.shape[1], frame.shape[0]

        # Define the corners of the big marker
        big_marker_corners = [
            marker_corners_dict[markerBR][2],  # TL = 0
            marker_corners_dict[markerTR][1],  # BL = 3
            marker_corners_dict[markerTL][0],  # BR = 2
            marker_corners_dict[markerBL][3],  # TR = 1
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
        warped_frame = cv2.warpPerspective(frame, matrix, (frame_width, frame_height))

        # Display the original and warped frames
        # cv2.imshow("Original Frame", frame)
        cv2.imshow("Warped Frame Inside ArUco Boundary", warped_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
