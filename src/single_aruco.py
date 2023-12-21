import cv2
import cv2.aruco as aruco
import numpy as np
import platform

# Mqtt
import paho.mqtt.publish as publish
import time

broker_address = "192.168.35.190"
led_topic = "led"
led_topic2 = "led2"
# Mqtt  end

# Define the dictionary to use
dictionary_to_use = cv2.aruco.DICT_6X6_250

# setting the url for ipcam
url = "http://192.168.1.30:4747/video"

# Initialize the camera
cap = None

if platform.system() == "Linux":
    # Try camera indices
    for i in range(1, 3):
        cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
        if cap.isOpened():
            print(f"Opened camera at index {i} using V4L2.")
            break
    else:
        print("No live stream found using camera indices. Trying URL...")

elif platform.system() == "Windows":
    # Try camera indices
    for i in range(1, 3):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Opened camera at index {i}.")
            break
    else:
        print("No live stream found using camera indices. Trying URL...")

# If camera is still not opened, try using the URL
if cap is None or not cap.isOpened():
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        if platform.system() == "Linux":
            cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        elif platform.system() == "Windows":
            cap = cv2.VideoCapture(0)
        else:
            print("No Supported Platform Found")

# Font to display
font = cv2.FONT_HERSHEY_COMPLEX

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print(
            "No live stream found. Ensure that you have selected correct camera. Exiting ..."
        )
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply threshold to the grayscale image
    _, threshold = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)

    # Detecting contours in frame
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Load the predefined dictionary for ArUco markers
    dictionary = aruco.getPredefinedDictionary(dictionary_to_use)

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
            if 2 in ids:
                publish.single(led_topic, "onn", hostname=broker_address)

            if 3 in ids:
                publish.single(led_topic2, "on", hostname=broker_address)

            if 4 in ids:
                publish.single(led_topic, "offf", hostname=broker_address)

            if 5 in ids:
                publish.single(led_topic2, "off", hostname=broker_address)
            # Mqtt end

    # Display the frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
