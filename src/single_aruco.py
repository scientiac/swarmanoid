import cv2
import cv2.aruco as aruco
import numpy as np
import platform

# Define the dictionary to use
dictionary_to_use = cv2.aruco.DICT_6X6_250

# Initialize the camera
# Handle the case where the operating system is neither Linux nor Windows
if platform.system() == "Linux":
    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
elif platform.system() == "Windows":
    cap = cv2.VideoCapture(0)
else:
    print("Unsupported operating system.")

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
            print(f"Marker {ids[i]} coordinates: {corner}")

            # Convert corners to int, as they are returned as float
            corner = corner.astype(int)

            # Draw boundary of ArUco marker
            cv2.polylines(frame, [corner[0]], True, (0, 0, 255), 1)

            # Draw coordinates of ArUco marker
            for point in corner[0]:
                x, y = point
                string = str(x) + " " + str(y)
                cv2.putText(frame, string, (x, y), font, 0.5, (0, 255, 0))

    # Display the frame
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
