import cv2
import cv2.aruco as aruco
import numpy as np

from micropython.secrets import BROKER_ADDRESS
from camera import detect_camera

import paho.mqtt.publish as publish
import time
from mqtt import establish_connection

# broker_address = BROKER_ADDRESS
led_topic = "led"
client = establish_connection()

# Define the dictionaries to try

dictionaries_to_try = [
    # cv2.aruco.DICT_4X4_50,
    # cv2.aruco.DICT_4X4_100,
    # cv2.aruco.DICT_4X4_250,
    # cv2.aruco.DICT_4X4_1000,
    # cv2.aruco.DICT_5X5_50,
    # cv2.aruco.DICT_5X5_100,
    # cv2.aruco.DICT_5X5_250,
    # cv2.aruco.DICT_5X5_1000,
    # cv2.aruco.DICT_6X6_50,
    # cv2.aruco.DICT_6X6_100,
    cv2.aruco.DICT_6X6_250,
    # cv2.aruco.DICT_6X6_1000,
    # cv2.aruco.DICT_7X7_50,
    # cv2.aruco.DICT_7X7_100,
    # cv2.aruco.DICT_7X7_250,
    # cv2.aruco.DICT_7X7_1000,
    # cv2.aruco.DICT_ARUCO_ORIGINAL,
    # # April Tag
    # cv2.aruco.DICT_APRILTAG_16h5,
    # cv2.aruco.DICT_APRILTAG_25h9,
    # cv2.aruco.DICT_APRILTAG_36h10,
    # cv2.aruco.DICT_APRILTAG_36h11,
]

cap = detect_camera()

# Font to display
font = cv2.FONT_HERSHEY_COMPLEX

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

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
        if ids is not None and len(ids) > 0:
            aruco.drawDetectedMarkers(frame, corners, ids)
            for i, corner in enumerate(corners):
                print(f"Marker {ids[i]} \ncoordinates: \n{corner}")

                # Convert corners to int, as they are returned as float
                corner = corner.astype(int)

                # Draw boundary of ArUco marker
                cv2.polylines(frame, [corner[0]], True, (0, 0, 255), 1)

                # Draw coordinates of ArUco marker
                for point in corner[0]:
                    x, y = point
                    string = str(x) + " " + str(y)
                    cv2.putText(frame, string, (x, y), font, 0.5, (255, 0, 0))

                # Mqtt
                if 4 in ids:
                    client.publish(led_topic, "on")

                if 5 in ids:
                    client.publish(led_topic, "off")
                # Mqtt end

    # Display the frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
