#!/usr/bin/env python

import cv2
import cv2.aruco as aruco
import numpy as np

# Define the dictionaries to try

# dictionaries_to_try = [
#     cv2.aruco.DICT_4X4_50,
#     cv2.aruco.DICT_4X4_100,
#     cv2.aruco.DICT_4X4_250,
#     cv2.aruco.DICT_4X4_1000,
#     cv2.aruco.DICT_5X5_50,
#     cv2.aruco.DICT_5X5_100,
#     cv2.aruco.DICT_5X5_250,
#     cv2.aruco.DICT_5X5_1000,
#     cv2.aruco.DICT_6X6_50,
#     cv2.aruco.DICT_6X6_100,
#     cv2.aruco.DICT_6X6_250,
#     cv2.aruco.DICT_6X6_1000,
#     cv2.aruco.DICT_7X7_50,
#     cv2.aruco.DICT_7X7_100,
#     cv2.aruco.DICT_7X7_250,
#     cv2.aruco.DICT_7X7_1000,
#     cv2.aruco.DICT_ARUCO_ORIGINAL,
#     # April Tag
#     cv2.aruco.DICT_APRILTAG_16h5,
#     cv2.aruco.DICT_APRILTAG_25h9,
#     cv2.aruco.DICT_APRILTAG_36h10,
#     cv2.aruco.DICT_APRILTAG_36h11,
# ]


dictionaries_to_try = [
    cv2.aruco.DICT_4X4_50,
    cv2.aruco.DICT_4X4_100,
    cv2.aruco.DICT_4X4_250,
    cv2.aruco.DICT_4X4_1000,
]

# Initialize the camera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Try detecting markers from different dictionaries and sizes
    for dictionary_id in dictionaries_to_try:
        # Load the predefined dictionary for ArUco markers
        dictionary = aruco.getPredefinedDictionary(dictionary_id)

        # Create an ArUco marker board
        board = aruco.CharucoBoard((3, 3), 0.04, 0.01, dictionary)

        # Detect ArUco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary)

        # Draw the markers on the frame
        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)

            # Estimate the pose of the markers
            retval, charucoCorners, charucoIds = aruco.interpolateCornersCharuco(
                corners, ids, gray, board
            )

            if retval > 0:
                aruco.drawDetectedCornersCharuco(frame, charucoCorners, charucoIds)

                # Estimate the pose of the board
                _, rvec, tvec = aruco.estimatePoseCharucoBoard(
                    charucoCorners,
                    charucoIds,
                    board,
                    cameraMatrix=None,
                    distCoeffs=None,
                )

                # Draw the pose information
                aruco.drawAxis(
                    frame,
                    cameraMatrix=None,
                    distCoeffs=None,
                    rvec=rvec,
                    tvec=tvec,
                    length=0.1,
                )

    # Display the frame
    # cv2.imshow("ArUco Marker Detection", cv2.flip(frame, 1))
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
