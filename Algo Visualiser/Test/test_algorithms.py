import pytest
import pygame
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Algos import h, A_star, DFS, BFS, dijkstra
from Node import Node

@pytest.fixture(scope="function", autouse=True)
def pygame_init_and_quit():
    pygame.init()
    pygame.display.set_mode((100, 100))
    yield
    pygame.quit()

def create_test_grid():
    grid = [[Node(i, j, 1, 1) for j in range(5)] for i in range(5)]

    # Make some nodes barriers
    for i in range(1, 4):
        grid[1][i].make_barrier()
        grid[3][i].make_barrier()

    return grid

def set_neighbours(grid):
    for i, row in enumerate(grid):
        for j, node in enumerate(row):
            if i > 0:
                node.neighbours.append(grid[i - 1][j])
            if i < len(grid) - 1:
                node.neighbours.append(grid[i + 1][j])
            if j > 0:
                node.neighbours.append(grid[i][j - 1])
            if j < len(row) - 1:
                node.neighbours.append(grid[i][j + 1])

def node_draw_func(_):
    pass

def update_display_func():
    pass

def test_h():
    p1 = (2, 3)
    p2 = (4, 7)
    assert h(p1, p2) == 6

def test_A_star():
    grid = create_test_grid()
    set_neighbours(grid)
    start = grid[0][0]
    end = grid[4][4]
    result = A_star(grid, start, end, node_draw_func, update_display_func)
    print(f"Start: {start.get_pos()}, End: {end.get_pos()}, Result: {result}")
    assert result == True

def test_DFS():
    grid = create_test_grid()
    set_neighbours(grid)
    start = grid[0][0]
    end = grid[4][4]
    result = DFS(grid, start, end, node_draw_func, update_display_func)
    print(f"Start: {start.get_pos()}, End: {end.get_pos()}, Result: {result}")
    assert result == True

def test_BFS():
    grid = create_test_grid()
    set_neighbours(grid)
    start = grid[0][0]
    end = grid[4][4]
    result = BFS(grid, start, end, node_draw_func, update_display_func)
    print(f"Start: {start.get_pos()}, End: {end.get_pos()}, Result: {result}")
    assert result == True

def test_dijkstra():
    grid = create_test_grid()
    set_neighbours(grid)
    start = grid[0][0]
    end = grid[4][4]
    result = dijkstra(grid, start, end, node_draw_func, update_display_func)
    print(f"Start: {start.get_pos()}, End: {end.get_pos()}, Result: {result}")
    assert result == True
