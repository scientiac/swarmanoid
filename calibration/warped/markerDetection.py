#!/usr/bin/env python

import cv2
import numpy as np
import cv2.aruco as aruco
from frameCorrection import get_warped_frame

# Example usage:
# url = "http://127.0.0.1:5000/video_feed"
url = "http://192.168.1.105:4747/video"
# url = "http://192.168.1.105:4747/video?1280x720"

# cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap = cv2.VideoCapture(url)

markerTL = 3
markerTR = 5
markerBL = 2
markerBR = 4

# Define the markers and their positions
marker_ids = [markerTL, markerTR, markerBL, markerBR]

# Define the dictionary to use
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Create ArUco parameters
parameters = cv2.aruco.DetectorParameters()

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    warped_frame, marker_corners_dict = get_warped_frame(frame, marker_ids, 10)

    if warped_frame is not None:
        # Detect markers within the warped frame
        corners, ids, _ = cv2.aruco.detectMarkers(
            warped_frame, aruco_dict, parameters=parameters
        )

        # Draw markers on the warped frame
        if ids is not None:
            for i in range(len(ids)):
                # Draw a rectangle around the detected marker
                # cv2.polylines(
                #     warped_frame, [np.int32(corners[i])], True, (0, 255, 0), 2
                # )
                image = aruco.drawDetectedMarkers(warped_frame, corners, ids)

        # Display the result
        cv2.imshow("Detected Markers in Warped Frame", image)
        cv2.imshow("Detected Markers", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
