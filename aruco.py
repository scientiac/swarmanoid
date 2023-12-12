#!/usr/bin/env python

import cv2
import cv2.aruco as aruco
import numpy as np
import networkx as nx

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
    cv2.aruco.DICT_6X6_250,
]

# Initialize the camera
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Define marker IDs for pathfinding
start_id = 1
end_id = 2

# Create a graph to represent marker connections
graph = nx.Graph()

# Define boundary marker IDs
boundary_marker_ids = {8, 7, 9, 10}

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

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

        if ids is not None:
            aruco.drawDetectedMarkers(frame, corners, ids)

            # Update the graph with marker connections
            if (
                len(ids) >= 3
            ):  # Only update the graph if three or more markers are detected
                # Clear the graph before updating with new connections
                graph.clear()

                # Add boundary markers to the graph
                for boundary_id in boundary_marker_ids:
                    if boundary_id in ids.flatten():
                        graph.add_node(boundary_id)

                # Connect boundary markers with lines from their centers
                for i in range(len(boundary_marker_ids)):
                    start_id = list(boundary_marker_ids)[i]
                    end_id = list(boundary_marker_ids)[
                        (i + 1) % len(boundary_marker_ids)
                    ]
                    if start_id in ids.flatten() and end_id in ids.flatten():
                        start_center = np.mean(
                            corners[ids.flatten().tolist().index(start_id)][0], axis=0
                        )
                        end_center = np.mean(
                            corners[ids.flatten().tolist().index(end_id)][0], axis=0
                        )
                        start_center = tuple(map(int, start_center))
                        end_center = tuple(map(int, end_center))
                        cv2.line(frame, start_center, end_center, (0, 0, 255), 2)

                for i in range(len(ids)):
                    for j in range(i + 1, len(ids)):
                        # Avoid adding connections for markers with ID 0
                        if ids[i][0] != 0 and ids[j][0] != 0:
                            # Avoid crossing the boundary
                            if (
                                ids[i][0] not in boundary_marker_ids
                                or ids[j][0] not in boundary_marker_ids
                            ):
                                graph.add_edge(ids[i][0], ids[j][0])

                # Check if the start and end markers are in the graph
                if start_id in graph.nodes() and end_id in graph.nodes():
                    try:
                        # Find the shortest path avoiding markers with ID 0 and crossing the boundary
                        path = nx.shortest_path(graph, source=start_id, target=end_id)

                        # Print the path
                        print("Shortest path:", path)

                        # Draw the path on the frame
                        for i in range(len(path) - 1):
                            try:
                                start_center = np.mean(
                                    corners[ids.flatten().tolist().index(path[i])][0],
                                    axis=0,
                                )
                                end_center = np.mean(
                                    corners[ids.flatten().tolist().index(path[i + 1])][
                                        0
                                    ],
                                    axis=0,
                                )
                                start_center = tuple(map(int, start_center))
                                end_center = tuple(map(int, end_center))
                                cv2.line(
                                    frame, start_center, end_center, (0, 255, 0), 2
                                )
                            except ValueError:
                                # Handle the case when the marker is not found in the list
                                pass
                    except nx.NetworkXNoPath:
                        print(
                            "No path found between {} and {}".format(start_id, end_id)
                        )
                else:
                    print("Start or end marker not detected.")
            else:
                print("Less than three markers detected. Not updating the graph.")

    # Display the frame
    # cv2.imshow("ArUco Marker Detection", cv2.flip(frame, 1))
    cv2.imshow("ArUco Marker Detection", frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
