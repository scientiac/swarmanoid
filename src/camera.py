import cv2
import platform


def detect_camera():
    # setting the url for ipcam
    url = "http://0.0.0.0:5000/video_feed"

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

    elif platform.system() == "Darwin":
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
        # if not fallback to default webcam.
        if not cap.isOpened():
            if platform.system() == "Linux":
                cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
            elif platform.system() == "Windows":
                cap = cv2.VideoCapture(0)
            elif platform.system() == "Darwin":
                cap = cv2.VideoCapture(0)
            else:
                print("No Supported Platform Found")

    return cap
