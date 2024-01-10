import cv2
import numpy as np
import cv2.aruco as aruco

def get_warped_frame(input_frame, marker_ids):
    # Load camera parameters from YAML file
    fs = cv2.FileStorage("miatoll.yml", cv2.FILE_STORAGE_READ)
    camera_matrix = fs.getNode("new_matrix").mat()
    dist_coefficients = fs.getNode("distortion_coef").mat()
    fs.release()

    # Detect markers in the frame
    corners, ids, _ = cv2.aruco.detectMarkers(
        input_frame, aruco_dict, parameters=parameters
    )

    marker_corners_dict = {marker_id: None for marker_id in marker_ids}

    if ids is not None:
        # Extract corners of the specified markers
        for marker_id in marker_ids:
            index = np.where(ids == marker_id)
            if len(index[0]) > 0:
                marker_corners_dict[marker_id] = corners[index[0][0]][0]

    # Check if all specified markers are detected
    if all(value is not None for value in marker_corners_dict.values()):
        # Get the width and height of the frame
        frame_width, frame_height = input_frame.shape[1], input_frame.shape[0]

        # Define the corners of the big marker
        big_marker_corners = [
            marker_corners_dict[marker_ids[3]][2],  # TL = 0
            marker_corners_dict[marker_ids[1]][1],  # BL = 3
            marker_corners_dict[marker_ids[0]][0],  # BR = 2
            marker_corners_dict[marker_ids[2]][3],  # TR = 1
        ]

        # # Calculate perspective transformation matrix
        # matrix = cv2.getPerspectiveTransform(
        #     np.float32(big_marker_corners),
        #     np.float32(
        #         [
        #             [frame_width, frame_height],
        #             [frame_width, 0],
        #             [0, 0],
        #             [0, frame_height],
        #         ]
        #     ),
        # )

        square_size = min(frame_width, frame_height)
        destination_points = np.float32([
            [square_size, square_size],
            [square_size, 0],
            [0, 0],
            [0, square_size],
        ])

        # Calculate perspective transformation matrix
        matrix = cv2.getPerspectiveTransform(
            np.float32(big_marker_corners),
            destination_points
        )

        # Warp the frame using the perspective transformation matrix
        warped_frame = cv2.warpPerspective(
            input_frame, matrix, (frame_width, frame_height)
        )

        return warped_frame, marker_corners_dict

    return None, None  # Return None if not all markers are detected

# Example usage:
# Define the dictionary to use
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Create ArUco parameters
parameters = cv2.aruco.DetectorParameters()
