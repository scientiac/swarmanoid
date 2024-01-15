#!/usr/bin/env python

import cv2
import cv2.aruco as aruco
import numpy as np
import heapq
import math

from marker_detection import detect_markers, find_nearest_marker_from_bot

# url = "http://127.0.0.1:5000/video_feed"  # Replace with your video feed URL
#
# # Boundary IDs
# markerTL = 1
# markerTR = 2
# markerBL = 4
# markerBR = 3
#
# # Define the boundary markers and their positions
# boundary_ids = [markerTL, markerTR, markerBL, markerBR]
#
# # Define the dictionary to use
aruco_dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
#
# # Define bot's ID
# bot_id = 69
# red_area = 33
# green_area = 22
#
# # ArUco marker dictionary and parameters
aruco_params = cv2.aruco.DetectorParameters()

# Define the grid size and marker dimensions
MARKER_SIZE = 150

# marker_positions = detect_markers(url, boundary_ids, aruco_dictionary)

# GRID_SIZE = 1000
# chosen_marker, waste_marker_ids = find_nearest_marker_from_bot(
#     marker_positions, bot_id, boundary_ids, red_area, green_area
# )

# Define obstacle IDs
# waste_marker_ids = [111, 122, 133, 69, 155, 166, 177, 188, 199, 100]

# Initialize the video capture
# url = "http://127.0.0.1:5000/video_feed"
# url = "http://192.168.1.105:4747/video"


def find_path(
    GRID_SIZE,
    marker_positions,
    chosen_marker,
    waste_marker_ids,
    url,
    bot_id,
):
    # Aruco detection
    cap = cv2.VideoCapture(url)

    # Define the window size for visualization
    WINDOW_SIZE = 740

    # Initialize the start and goal positions
    start_position = None
    goal_position = None

    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Define the A* algorithm
    def astar(start, goal, grid):
        # Define the heuristic function

        # Manhattan Distance
        # def heuristic(a, b):
        #     return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Euclidean Distance
        def heuristic(a, b):
            return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

        # Diagonal Distance
        # def heuristic(a, b):
        #     dx = abs(a[0] - b[0])
        #     dy = abs(a[1] - b[1])
        #     return max(dx, dy)

        # Chebyshev Distance
        # def heuristic(a, b):
        #     dx = abs(a[0] - b[0])
        #     dy = abs(a[1] - b[1])
        #     return max(dx, dy, dx + dy)

        # Define the neighbors function
        def neighbors(position):
            x, y = position
            # candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            candidates = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
                (x - 1, y - 1),
                (x - 1, y + 1),
                (x + 1, y - 1),
                (x + 1, y + 1),
            ]

            valid_neighbors = []
            for neighbor in candidates:
                nx, ny = neighbor
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] != 1:
                    valid_neighbors.append(neighbor)
            return valid_neighbors

        # Initialize the data structures
        open_set = []
        closed_set = set()
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}

        # Add the start position to the open set
        heapq.heappush(open_set, (f_score[start], start))

        while open_set:
            # Get the position with the lowest f-score from the open set
            current = heapq.heappop(open_set)[1]

            if current == goal:
                # Reconstruct the path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path

            # Add the current position to the closed set
            closed_set.add(current)

            # Explore the neighbors
            for neighbor in neighbors(current):
                neighbor_g_score = g_score[current] + 1

                if neighbor in closed_set:
                    continue

                if neighbor not in open_set or neighbor_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = neighbor_g_score
                    f_score[neighbor] = neighbor_g_score + heuristic(neighbor, goal)
                    if neighbor not in open_set:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        # No path found
        return None

    while True:
        # Read a frame from the video capture
        ret, frame = cap.read()

        if not ret:
            break

        # Resize the frame for visualization
        # frame = cv2.resize(frame, (WINDOW_SIZE, WINDOW_SIZE))

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers in the frame
        corners, ids, _ = cv2.aruco.detectMarkers(
            gray, aruco_dictionary, parameters=aruco_params
        )

        # Draw the detected markers on the frame
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            # Find the start and goal positions
            for i in range(len(ids)):
                marker_id = ids[i][0]
                marker_corners = corners[i][0]

                # Calculate the marker position in the grid
                marker_center = np.mean(marker_corners, axis=0)
                marker_x, marker_y = marker_center[0], marker_center[1]
                grid_x = int(marker_x * GRID_SIZE / WINDOW_SIZE)
                grid_y = int(marker_y * GRID_SIZE / WINDOW_SIZE)

                # Set the start and goal positions based on the marker IDs
                if marker_id == bot_id:
                    start_position = (grid_x, grid_y)
                elif marker_id == chosen_marker:
                    goal_position = (grid_x, grid_y)

                # Mark obstacle positions based on obstacle IDs
                elif marker_id in waste_marker_ids:
                    # Calculate the marker position in the grid
                    marker_area = cv2.contourArea(marker_corners)
                    marker_radius = int(np.sqrt(marker_area / np.pi))
                    for dx in range(-marker_radius, marker_radius + 1):
                        for dy in range(-marker_radius, marker_radius + 1):
                            nx, ny = grid_x + dx, grid_y + dy
                            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                                grid[nx][ny] = 1

        # Find the path using A*
        if start_position is not None and goal_position is not None:
            # Create the grid
            # grid = np.zeros((GRID_SIZE, GRID_SIZE))
            # print(grid)

            # Find the path
            path = astar(start_position, goal_position, grid)
            # return path

            # Draw the path on the frame
            if path is not None:
                for i in range(len(path) - 1):
                    position_a = path[i]
                    position_b = path[i + 1]
                    x1 = int((position_a[0] + 0.5) * WINDOW_SIZE / GRID_SIZE)
                    y1 = int((position_a[1] + 0.5) * WINDOW_SIZE / GRID_SIZE)
                    x2 = int((position_b[0] + 0.5) * WINDOW_SIZE / GRID_SIZE)
                    y2 = int((position_b[1] + 0.5) * WINDOW_SIZE / GRID_SIZE)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), thickness=2)

            print(path)
            # return path

        # Display the frame
        cv2.imshow("Path Planning", frame)

        # Check for key press
        if cv2.waitKey(1) == ord("q"):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()


# find_path(
#     GRID_SIZE,
#     marker_positions,
#     chosen_marker,
#     waste_marker_ids,
#     aruco_params,
#     url,
#     bot_id,
# )
