import sys
import os
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Node import Node

def test_update_neighbours():
    # Create a 3x3 grid
    grid = [[Node(x, y, 10, 3) for y in range(3)] for x in range(3)]

    # Make the center node a barrier
    grid[1][1].make_barrier()

    # Update the neighbors of the top-left node
    grid[0][0].update_neighbours(grid)

    # Check that the barrier node is not a neighbor
    assert grid[1][1] not in grid[0][0].neighbours

    # Check that the correct nodes are neighbors
    expected_neighbours = [grid[0][1], grid[1][0]]
    assert set(grid[0][0].neighbours) == set(expected_neighbours)
