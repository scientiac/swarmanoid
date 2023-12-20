import cv2
import cv2.aruco as aruco
import numpy as np
import platform

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
    cv2.aruco.DICT_6X6_50,
    cv2.aruco.DICT_6X6_100,
    cv2.aruco.DICT_6X6_250,
    cv2.aruco.DICT_6X6_1000,
]

# setting the url for ipcam
url = "http://192.168.1.105:4747/video"

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
                    cv2.putText(frame, string, (x, y), font, 0.5, (0, 255, 0))

    # Display the frame
    # cv2.imshow("ArUco Marker Detection", cv2.flip(frame, 1))
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
