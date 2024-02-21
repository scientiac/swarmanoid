import cv2
import cv2.aruco as aruco
import numpy as np
import time

from camera import detect_camera
from mqtt import establish_connection

topic_wave = "wave"
topic_particle = "particle"

client = establish_connection()

# Load camera parameters from YAML file
fs = cv2.FileStorage("miatoll.yml", cv2.FILE_STORAGE_READ)
camera_matrix = fs.getNode("new_matrix").mat()
dist_coefficients = fs.getNode("distortion_coef").mat()
fs.release()

# Dictionary to store marker IDs and their midpoints
marker_midpoints = {}

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

        parameters = aruco.DetectorParameters()

        # Detect ArUco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dictionary)

        # Draw the markers on the frame
        if ids is not None and len(ids) > 0:
            aruco.drawDetectedMarkers(frame, corners, ids)

            for i, corner in enumerate(corners):
                # Convert corners to int, as they are returned as float
                corner = corner.astype(int)

                # Draw boundary of ArUco marker
                cv2.polylines(frame, [corner[0]], True, (0, 0, 255), 1)

                # Calculate midpoint of the top edge
                top_midpoint = tuple(np.mean(corner[0][:2], axis=0).astype(int))

                mid_center = tuple(np.mean(corner[0], axis=0).astype(int))

                cv2.circle(frame, mid_center, 3, (255, 0, 0), -1)

                # Draw arrow pointing to the top edge
                cv2.arrowedLine(
                    frame,
                    mid_center,
                    top_midpoint,
                    (0, 255, 0),
                    2,
                    tipLength=2,
                )

                # Store marker ID and midpoint in the dictionary
                marker_id = ids[i][0]
                marker_midpoints[marker_id] = top_midpoint

                # Access angle relative to the arena
                if marker_id in [69, 96, 1, 2, 3, 4]:
                    angle_rad = np.arctan2(
                        top_midpoint[1] - mid_center[1],
                        top_midpoint[0] - mid_center[0],
                    )

                    angle_deg = np.degrees(angle_rad)
                    # Ensure the angle is between 0 and 360
                    angle_deg = int(abs(angle_deg + 180)) % 360
                    int_angle_deg = angle_deg

                    print(f"Marker {marker_id} angle: {int_angle_deg} degrees")

                # Draw coordinates of ArUco marker
                # for point in corner[0]:
                #     x, y = point
                #     string = str(x) + " " + str(y)
                #     cv2.putText(frame, string, (x, y), font, 0.5, (255, 0, 0))

                # Mqtt

                # client.publish(topic_wave, "right")

                # counter = 0
                # while counter < 100:
                #     client.publish(topic_particle, "down")
                #     counter += 1

                # # Mqtt
                # counter = 0
                # while counter < 100:
                #     client.publish(topic_wave, "left")
                #     counter += 1

                # counter = 0
                # while counter < 100:
                #     client.publish(topic_particle, "up")
                #     counter += 1

                # Mqtt end

    # Display the frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
