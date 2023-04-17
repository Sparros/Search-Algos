import pygame
import sys
import os
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Node import Node

def test_get_pos():
    # Test that get_pos() returns the correct row and column
    node = Node(1, 2, 10, 20)
    assert node.get_pos() == (1, 2)

def test_is_empty():
    # Test that a newly created node is empty
    node = Node(1, 2, 10, 20)
    assert node.is_empty() == True

def test_is_closed():
    # Test that make_closed() sets the node's color to RED
    node = Node(1, 2, 10, 20)
    node.make_closed()
    assert node.is_closed() == True

def test_is_open():
    # Test that make_open() sets the node's color to GREEN
    node = Node(1, 2, 10, 20)
    node.make_open()
    assert node.is_open() == True

def test_is_barrier():
    # Test that make_barrier() sets the node's color to BLACK
    node = Node(1, 2, 10, 20)
    node.make_barrier()
    assert node.is_barrier() == True

def test_is_start():
    # Test that make_start() sets the node's color to ORANGE
    node = Node(1, 2, 10, 20)
    node.make_start()
    assert node.is_start() == True

def test_is_end():
    # Test that make_end() sets the node's color to TURQUOISE
    node = Node(1, 2, 10, 20)
    node.make_end()
    assert node.is_end() == True

def test_is_traffic():
    # Test that make_traffic() sets the node's color to YELLOW
    node = Node(1, 2, 10, 20)
    node.make_traffic()
    assert node.is_traffic() == True

def test_reset():
    # Test that reset() sets the node's color to WHITE
    node = Node(1, 2, 10, 20)
    node.make_closed()
    node.reset()
    assert node.is_empty() == True

def test_update_neighbours():
    # Test that update_neighbours() adds the correct neighbours to the node's neighbours list
    grid = [[Node(0, 0, 10, 10), Node(0, 1, 10, 10)], [Node(1, 0, 10, 10), Node(1, 1, 10, 10)]]
    node = grid[0][0]
    node.update_neighbours(grid)
    assert len(node.neighbours) == 2
    assert grid[1][0] in node.neighbours
    assert grid[0][1] in node.neighbours
