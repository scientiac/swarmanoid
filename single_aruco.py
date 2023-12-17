#!/usr/bin/env python

import cv2
import cv2.aruco as aruco
import numpy as np

# Define the dictionary to use
dictionary_to_use = cv2.aruco.DICT_6X6_250

# Initialize the camera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the predefined dictionary for ArUco markers
    dictionary = aruco.getPredefinedDictionary(dictionary_to_use)

    # Create an ArUco marker board
    board = aruco.CharucoBoard((3, 3), 0.04, 0.01, dictionary)

    # Detect ArUco markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary)

    # Draw the markers on the frame
    if ids is not None and len(ids) > 0:
        aruco.drawDetectedMarkers(frame, corners, ids)

    # Display the frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
v2.destroyAllWindows()
