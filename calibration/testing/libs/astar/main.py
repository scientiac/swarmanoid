#!/usr/bin/env python

from library import find_path

# Define the initial grid
GRID_SIZE = 1000
initial_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# Define the start and goal positions
start_position = 69
waste_marker_positions = [144, 133]
goal_position = 155

# Call the find_path function
find_path(start_position, waste_marker_positions, goal_position, initial_grid)
