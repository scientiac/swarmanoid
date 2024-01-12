import cv2
import cv2.aruco as aruco
import numpy as np
import heapq


def find_path(start_position, waste_marker_positions, goal_position, initial_grid):
    # Define the A* algorithm
    def astar(start, goal, grid):
        # Define the heuristic function (Manhattan distance)
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        # Define the neighbors function
        def neighbors(position):
            x, y = position
            candidates = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
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

    # Boundary IDs
    markerTL = 1
    markerTR = 2
    markerBL = 4
    markerBR = 3

    # Define the boundary markers and their positions
    boundary_ids = [markerTL, markerTR, markerBL, markerBR]

    # Define the dictionary to use
    aruco_dictionary = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

    # Define the grid size and marker dimensions
    GRID_SIZE = len(initial_grid)

    # Define the window size for visualization
    WINDOW_SIZE = 740

    # Initialize the start and goal positions
    start_position = start_position
    goal_position = goal_position

    grid = initial_grid

    # Aruco detection
    cap = cv2.VideoCapture(0)  # Replace with your video capture source

    # Aruco marker dictionary and parameters
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    aruco_params = cv2.aruco.DetectorParameters()

    while True:
        # Read a frame from the video capture
        url = "http://127.0.0.1:5000/video_feed"
        cap = cv2.VideoCapture(url)  # Change 0 to your camera index or video file path
        ret, frame = cap.read()

        if not ret:
            break

        # Resize the frame for visualization
        frame = cv2.resize(frame, (WINDOW_SIZE, WINDOW_SIZE))

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect ArUco markers in the frame
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

        # Find the start and goal positions
        start_positions = []
        for i in range(len(ids)):
            marker_id = ids[i][0]
            marker_corners = corners[i][0]
            
            # Calculate the marker position in the grid
            marker_center = np.mean(marker_corners, axis=0)
            marker_x, marker_y = marker_center[0], marker_center[1]
            grid_x = int(marker_x * GRID_SIZE / WINDOW_SIZE)
            grid_y = int(marker_y * GRID_SIZE / WINDOW_SIZE)
            
            # Mark obstacle positions based on marker IDs
            if marker_id in waste_marker_positions:
                grid[grid_x][grid_y] = 1

            if marker_id == start_position:
                start_positions.append((grid_x, grid_y))

            if marker_id == goal_position:
                goal_position = (grid_x, grid_y)

        # Find the path using A*
        paths = []
        for start_pos in start_positions:
            path = astar(start_pos, goal_position, grid)
            if path:
                paths.append(path)

        # Draw the paths on the frame
        if paths:
            for path in paths:
                for position in path:
                    x, y = position
                    x_pixel = int(x * WINDOW_SIZE / GRID_SIZE)
                    y_pixel = int(y * WINDOW_SIZE / GRID_SIZE)
                    cv2.circle(frame, (x_pixel, y_pixel), 5, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow("Aruco Marker Detection", frame)

        # Exit if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture
    cap.release()

    # Destroy all windows
    cv2.destroyAllWindows()

