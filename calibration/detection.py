#!/usr/bin/env python

import cv2
import numpy as np
import cv2.aruco as aruco

url = "http://192.168.1.105:4747/video"

# Aruco detection
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
    arucoParameters = aruco.DetectorParameters()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(
        gray, aruco_dict, parameters=arucoParameters
    )
    print(ids)
    if np.all(ids):
        image = aruco.drawDetectedMarkers(frame, corners, ids)
        cv2.imshow("Display", image)
    else:
        display = frame
        cv2.imshow("Display", display)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
