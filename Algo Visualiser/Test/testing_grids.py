import sys
import os
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Main import create_single_grid, set_start_end, copy_grid, get_neighbours, carve_paths

@pytest.fixture
def grid():
    return create_single_grid(3, 300)

def test_get_neighbours():
    result = get_neighbours(0, 0)
    expected = [(2, 0, 1, 0), (0, 2, 0, 1)]
    assert result == expected

def test_carve_paths(grid):
    start = grid[0][0]
    end = grid[-1][-1]
    visited = set()
    carve_paths(start.row, start.col, visited)
    assert end in visited

def test_set_start_end(grid):
    start, end = set_start_end(grid, 0, 0, 2, 2)
    assert start.is_start()
    assert end.is_end()

def test_create_single_grid():
    grid = create_single_grid(3, 300)
    assert len(grid) == 3
    assert len(grid[0]) == 3
    assert grid[0][0].row == 0
    assert grid[0][0].col == 0
    assert grid[0][0].width == 100
    assert grid[0][0].total_rows == 3

def test_copy_grid(grid):
    grid_copy = copy_grid(grid)
    assert len(grid_copy) == 3
    assert len(grid_copy[0]) == 3
    assert grid_copy[0][0].row == 0
    assert grid_copy[0][0].col == 0
    assert grid_copy[0][0].width == 100
    assert grid_copy[0][0].total_rows == 3
    assert grid_copy[0][0].is_start() == False
    assert grid_copy[0][0].is_end() == False
    assert grid_copy[0][0].is_barrier() == False
    assert grid_copy[0][0].is_traffic() == False
