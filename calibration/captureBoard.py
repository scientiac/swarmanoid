#!/usr/bin/env python

import cv2
import numpy as np
import cv2.aruco as aruco
import time

url = "http://192.168.1.105:4747/video"

# Aruco detection
cap = cv2.VideoCapture(url)

last_recorded_time = time.time()
frame_count = 0

while True:
    _, frame = cap.read()
    curr_time = time.time()
    cv2.imshow("Display", frame)
    if curr_time - last_recorded_time >= 2.0:
        cv2.imwrite("images/frame_{}.png".format(frame_count), frame)
        last_recorded_time = curr_time
        frame_count += 1
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
