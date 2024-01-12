import aruco_utils
import path_planning
import robot_control
import pickup_detection


def main():
    # Initialize robot and necessary components

    while True:
        # Step 1: ArUco Marker Detection
        detected_markers = aruco_utils.detect_markers()

        if len(detected_markers) == 0:
            continue

        # Step 2: Navigation
        closest_marker = aruco_utils.find_closest_marker(detected_markers)
        path = path_planning.calculate_shortest_path(closest_marker)
        robot_control.follow_path(path)

        # Step 3: Marker Pickup
        pickup_detection.pickup_marker()

        # Step 4: Marker Verification
        if pickup_detection.is_marker_picked_up():
            # Step 5: Destination Marker Detection
            destination_markers = aruco_utils.detect_markers()

            if len(destination_markers) == 0:
                continue

            # Step 6: Destination Navigation
            destination_marker = aruco_utils.find_closest_marker(destination_markers)
            destination_path = path_planning.calculate_shortest_path(destination_marker)
            robot_control.follow_path(destination_path)

            # Step 7: Waste Dropping
            robot_control.drop_waste()

        # Repeat the loop for the next task


if __name__ == "__main__":
    main()
