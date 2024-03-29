import pygame
import random
from queue import PriorityQueue
from threading import Thread
from multiprocessing import Process
from queue import Queue
import sys

import Node
import Algos
#import help_window
from Menu import Menu
from help_window import open_help_window

# Initialize pygame
pygame.init()
pygame.display.set_caption("Algorithm Pathfinding")

PADDING = 20
MENU_WIDTH = 250
WIDTH = 750
HEIGHT = 750 
global ROWS 
ROWS = 25
FONT_SIZE = 24
FREE_DRAW_MODE = False
ALGORITHM_FUNCTIONS = {
    "A*": Algos.A_star,
    "DFS": Algos.DFS,
    "BFS": Algos.BFS,
    "Dijkstra": Algos.dijkstra,
    "Greedy Best-First": Algos.greedy_best_first,
    "Bidirectional BFS": Algos.bidirectional_bfs,
    "Jump Point Search": Algos.jps,
    "Bellman-Ford": Algos.bellman_ford
}

WIN = pygame.display.set_mode((MENU_WIDTH + WIDTH, HEIGHT))

MENU = pygame.Surface((MENU_WIDTH, HEIGHT))
# Initialize the menu
menu = Menu(MENU_WIDTH, HEIGHT)

GRID_SCREEN = pygame.Surface((WIDTH, HEIGHT))
GRID_SCREEN.fill((255, 255, 255))

# Divide the grid into 4 rectangular areas
GRID_WIDTH = ((WIDTH - (PADDING * 5)) // 2)  # Subtract the padding 5 times (2 side paddings, 2 middle paddings, 1 extra)
GRID_HEIGHT = ((HEIGHT - (PADDING * 3) - (FONT_SIZE * 2)) // 2)  # Subtract the font size + Padding to make room for the text + padding
top_left_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
top_right_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
bottom_left_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
bottom_right_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))

# Generate maze from 2D array of nodes
def generate_maze(grid, start, end, add_traffic, traffic_probability=0.1):
    # Fill the grid with barriers
    for row in grid:
        for node in row:
            if not node.is_start() and not node.is_end():
                node.make_barrier()

    def get_neighbours(x, y):
        neighbours = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbours.append((nx, ny, dx, dy))
        return neighbours

    # Recursively "carve paths" between the start and end nodes
    def carve_paths(x, y, visited):
        visited.add((x, y))
        if not grid[x][y].is_start() and not grid[x][y].is_end():
            grid[x][y].reset()
        neighbours = get_neighbours(x, y)
        random.shuffle(neighbours)

        for nx, ny, dx, dy in neighbours:
            if (nx, ny) not in visited:
                grid[x + dx][y + dy].reset()  
                carve_paths(nx, ny, visited)

    visited = set()
    carve_paths(start.row, start.col, visited)

    #print(add_traffic)
    if add_traffic:
        for row in grid:
            for node in row:
                if node.is_empty() and random.random() < traffic_probability:
                    node.make_traffic()

def set_start_end(grid, start_row, start_col, end_row, end_col):
    start = grid[start_row][start_col]
    end = grid[end_row][end_col]
    start.make_start()
    end.make_end()
    #print(f"Set start node: {start}, end node: {end}")
    return start, end

# Given row and width, create a 2D array of nodes
def create_single_grid(rows, width):
    gap = width // rows
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node.Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

# Given the number of rows and the width of a grid, creates a 2D list of Node objects representing the grid.
def create_and_copy_grids(rows, width, traffic):
    global FREE_DRAW_MODE
    base_grid = create_single_grid(rows, width)

    # If free draw mode is enabled, return the base grid to avoid setting start and end nodes
    if not FREE_DRAW_MODE:
        start_node, end_node = set_start_end(base_grid, 1, 1, rows - 2, rows - 2)
        generate_maze(base_grid, start_node, end_node, traffic)
    top_left_grid = copy_grid(base_grid)
    top_right_grid = copy_grid(base_grid)
    bottom_left_grid = copy_grid(base_grid)
    bottom_right_grid = copy_grid(base_grid)

    if FREE_DRAW_MODE:
        return top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, None, None
    #print(f"Grids created - start node: {start_node}, end node: {end_node}")
    return top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node

# iterate through grid and copy the nodes
def copy_grid(source_grid):
    copied_grid = []
    for i in range(len(source_grid)):
        copied_grid.append([])
        for j in range(len(source_grid[i])):
            node = Node.Node(source_grid[i][j].row, source_grid[i][j].col, source_grid[i][j].width, source_grid[i][j].total_rows)
            copied_grid[i].append(node)
            if source_grid[i][j].is_start():
                node.make_start()
            elif source_grid[i][j].is_end():
                node.make_end()
            elif source_grid[i][j].is_barrier():
                node.make_barrier()
            elif source_grid[i][j].is_traffic():
                node.make_traffic()
    return copied_grid

# Create the title surface to go above the grid
def create_title_surface(algorithm_name):
    title_surface = pygame.Surface((GRID_WIDTH, FONT_SIZE))
    title_surface.fill((255, 255, 255))
    title_font = pygame.font.SysFont("Arial", FONT_SIZE)
    if algorithm_name is not None:
        title_text = title_font.render(f"{algorithm_name} Search", 1, (0, 0, 0))
        title_surface.blit(title_text, (0, 0))
    return title_surface

# Draw the grid lines between the nodes
def draw_grid_lines(surface, rows, width):
    gap = width // rows
    for i in range(rows + 1):  # Change this line
        pygame.draw.line(surface, (128, 128, 128), (0, i * gap), (width, i * gap))
        pygame.draw.line(surface, (128, 128, 128), (i * gap, 0), (i * gap, width))

# Draw the grid
def draw(surface, grid, rows, width):
    #print("Drawing grid")
    #surface.fill((255,255,255))
    for row in grid:
        for node in row:
            node.draw(surface)
    
    draw_grid_lines(surface, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def free_draw(surface, grid, rows, width, start_end_nodes, x_offset, y_offset, clicked_surface=None):
    start, end = start_end_nodes
    node = None

    if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
        print("Left click")
        pos = pygame.mouse.get_pos()
        pos = (pos[0] - x_offset, pos[1] - y_offset)
        row, col = get_clicked_pos(pos, rows, width)

        keys = pygame.key.get_pressed()
        shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]

        if 0 <= row < rows and 0 <= col < rows:
            node = grid[row][col]
            if not start and not node.is_barrier() and not node.is_end():
                start = node
                start.make_start()
                start_end_nodes = (start, end)

            elif not end and node != start and not node.is_barrier() and not node.is_start():
                end = node
                end.make_end()
                start_end_nodes = (start, end)

            elif node != end and node != start and shift_pressed:
                node.make_traffic()
                
            elif node != end and node != start:
                node.make_barrier()

            if clicked_surface:
                node.draw(clicked_surface)

    elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
        print("Right click")
        pos = pygame.mouse.get_pos()
        pos = (pos[0] - x_offset, pos[1] - y_offset)
        row, col = get_clicked_pos(pos, rows, width)
        node = grid[row][col]
        node.reset()
        if node == start:
            start = None
            start_end_nodes = (start, end)
        elif node == end:
            end = None
            start_end_nodes = (start, end)

        if clicked_surface:
            node.draw(clicked_surface)

    return start_end_nodes, grid

def run_algorithms_sequentially(grids, start_node, end_node, selected_algorithms):
    # Create a list to hold the results of the algorithms
    results = []
    # Loop through each algorithm, grid and surface, running each algorithm sequentially
    for algo, grid, surface in zip(selected_algorithms, grids, [top_left_surf, top_right_surf, bottom_left_surf, bottom_right_surf]):
        # If the algorithm is not None, run it and append the result to the results list
        if algo is not None:
            result = ALGORITHM_FUNCTIONS[algo](grid, start_node, end_node, (lambda node: node.draw(surface)), update_display)
            results.append(result)
    # Print the results and return them
    print(results)
    return results

def run_algorithms_parallel(grids, start_node, end_node, selected_algorithms):
    surfaces = [top_left_surf, top_right_surf, bottom_left_surf, bottom_right_surf]
    # Create a list of threads to hold the running algorithms
    threads = []
    # Create a list to hold the results of the algorithms
    results = [None] * len(selected_algorithms)
    print(selected_algorithms, surfaces)
    # Loop through each algorithm, grid and surface, running each algorithm in parallel
    for i, (algo, grid, surface) in enumerate(zip(selected_algorithms, grids, surfaces)):
        # avoid running the algorithm if it is not selected
        if algo is not None:
            # Create a function to draw the node on the surface
            draw_function = lambda node, surface=surface: node.draw(surface)
            # Create a thread for the algorithm
            thread = Thread(target=algo_wrapper, args=(ALGORITHM_FUNCTIONS[algo], grid, start_node, end_node, draw_function, update_display, results, i))
            threads.append(thread)

    # Start all the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(f"Results: {results}")
    return results

# A wrapper to avoid changing all the algorithm functions for getting results with threading
def algo_wrapper(algo_function, grid, start, end, draw_func, update_display, results, index):
    result = algo_function(grid, start, end, draw_func, update_display)
    results[index] = result

def update_grids(surfaces, grids, rows, width, start_end_nodes):
    global FREE_DRAW_MODE
    # If the free draw mode is on, clear the grids and reset the start and end nodes
    if FREE_DRAW_MODE:
        for grid in grids:
            clear_grid(grid)
        start_end_nodes = (None, None)  
        start_node, end_node = start_end_nodes
    # If the free draw mode is off, set the start and end nodes
    else:
        start_node, end_node = set_start_end(grids[0], 1, 1, ROWS - 2, ROWS - 2)
    # Draw the grids on the surfaces and return the start and end nodes
    for surf, grid in zip(surfaces, grids):
        draw(surf, grid, rows, width)
    return start_node, end_node

def create_app(selected_algorithms):
    titles = []
    surfaces = [] 

    # Create title surfaces for selected algorithms
    for algo in selected_algorithms:
        if algo is not None:
            titles.append(create_title_surface(algo))
        else:
            empty_title = pygame.Surface((GRID_WIDTH, FONT_SIZE))
            empty_title.fill((255, 255, 255))
            titles.append(empty_title)

    positions = [
        (PADDING, PADDING),
        (GRID_WIDTH + PADDING * 3, PADDING),
        (PADDING, GRID_HEIGHT + PADDING * 2 + FONT_SIZE),
        (GRID_WIDTH + PADDING * 3, GRID_HEIGHT + PADDING * 2 + FONT_SIZE),
    ]

    # Assign title surfaces to their positions
    for title, pos in zip(titles, positions):
        surfaces.append((title, pos))

    # Blit the title surfaces onto the window
    for surface, pos in surfaces:
        GRID_SCREEN.blit(surface, pos)
    # Blit the title surfaces onto the window
    for surface, pos in surfaces:
        GRID_SCREEN.blit(surface, pos)
    
    # Blit the grid surfaces onto the window
    update_display()

    # Draw the menu
    WIN.blit(MENU, (0, 0))
    menu.draw(MENU)

    pygame.display.update()

# Called whenever the dispaly is changed i,e node change from algos running/free draw
def update_display():
    # Blit the grid surfaces onto the window
    GRID_SCREEN.blit(top_left_surf, (PADDING, PADDING + FONT_SIZE))
    GRID_SCREEN.blit(top_right_surf, (GRID_WIDTH + PADDING * 3, PADDING + FONT_SIZE))
    GRID_SCREEN.blit(bottom_left_surf, (PADDING, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2))
    GRID_SCREEN.blit(bottom_right_surf, (GRID_WIDTH + PADDING * 3, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2))
    WIN.blit(GRID_SCREEN, (MENU_WIDTH, 0))
    # Update the display
    pygame.display.flip()

# called by free draw button
def clear_grid(grid):
    for row in grid:
        for node in row:
            node.reset()

# called by reset button
def reset_grid(grid):
    for row in grid:
        for node in row:
            if not node.is_barrier() and not node.is_start() and not node.is_end():
                node.reset()

def main():  
    grid_needs_update = True
    execution_mode = "PARALLEL"
    start_end_nodes = (None, None)
    traffic = False
    global ROWS
    selected_algorithms = ["A*", "DFS", "BFS", "Dijkstra"]
    # for free draw mode
    global FREE_DRAW_MODE
    left_button_down = False
    right_button_down = False
    # initialise grids
    top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node = create_and_copy_grids(ROWS, GRID_WIDTH, traffic)

    surfaces = [top_left_surf, top_right_surf, bottom_left_surf, bottom_right_surf]
    grids = [top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid]

    while True:
        # updates display with correct grid titles, updates menu
        create_app(selected_algorithms)
        # called on maze change, row change
        if grid_needs_update:
            start_node, end_node = update_grids(surfaces, grids, ROWS, GRID_WIDTH, start_end_nodes)
            grid_needs_update = False

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Returns variables from menu changes
            action, traffic, new_rows, updated_algorithms = menu.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    left_button_down = True
                elif event.button == 3:  # Right mouse button
                    right_button_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    left_button_down = False
                elif event.button == 3:  # Right mouse button
                    right_button_down = False

            if (left_button_down or right_button_down) and FREE_DRAW_MODE:
                start_end_nodes, grids[0] = free_draw(top_left_surf, grids[0], ROWS, GRID_WIDTH, start_end_nodes, PADDING + MENU_WIDTH, PADDING + FONT_SIZE, top_left_surf)
                start_node, end_node = start_end_nodes
                
                for i, grid in enumerate(grids[1:], 1):
                    for row, source_row in zip(grid, grids[0]):
                        for node, source_node in zip(row, source_row):
                            if not node.is_same_state(source_node):  # Check if the source node's state is different from the current node
                                node.update_from(source_node)
                                node.draw(surfaces[i])
                update_display()

            # Remove unselected algorithms
            for i, algo in enumerate(selected_algorithms):
                if algo not in updated_algorithms:
                    selected_algorithms[i] = None

            # Add new algorithms
            new_algorithms = [algo for algo in updated_algorithms if algo not in selected_algorithms]
            for i, algo in enumerate(selected_algorithms):
                if algo is None and new_algorithms:
                    selected_algorithms[i] = new_algorithms.pop(0)
            #print(selected_algorithms)

            if action == "PARALLEL_EVENT":
                execution_mode = "PARALLEL"
            elif action == "SEQUENTIAL_EVENT":
                execution_mode = "SEQUENTIAL"

            elif action == "START_EVENT" or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                print("start event triggered")
                if start_node is None or end_node is None:
                    print("Start or end node is not set. Please set both nodes before running the algorithm.")
                    continue
                for grid in grids:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)       
                if execution_mode == "SEQUENTIAL":
                    results = run_algorithms_sequentially(grids, start_node, end_node, selected_algorithms)
                elif execution_mode == "PARALLEL":
                    results = run_algorithms_parallel(grids, start_node, end_node, selected_algorithms)
                menu.update_table(selected_algorithms, results)

            elif action == "RESET_EVENT":
                if FREE_DRAW_MODE:
                    start_node, end_node = None, None
                    start_end_nodes = (start_node, end_node)
                for grid in grids:
                    reset_grid(grid)
                start_node, end_node = set_start_end(grids[0], 1, 1, ROWS - 2, ROWS - 2)
                grid_needs_update = True

            elif action == "ROW_CHANGE_EVENT" and new_rows is not None:
                    ROWS = new_rows
                    top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node = create_and_copy_grids(ROWS, GRID_WIDTH, traffic)
                    grids = [top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid]
                    grid_needs_update = True 
                    if FREE_DRAW_MODE:
                        start_end_nodes = (None, None)
                        
            elif action == "NEW_MAZE_EVENT":
                top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node = create_and_copy_grids(ROWS, GRID_WIDTH, traffic)
                grids = [top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid]
                FREE_DRAW_MODE = False
                grid_needs_update = True

            elif action == "FREE_DRAW_EVENT":
                FREE_DRAW_MODE = not FREE_DRAW_MODE
                grid_needs_update = True

            elif action == "HELP_EVENT":
                # run help window on own process so both windows can be open at the same time
                # process instead of thread because of pygame issues 
                help_process = Process(target=open_help_window)
                help_process.start()

        # Update the menu and display
        menu.update(0.0)
        #pygame.display.update()

if __name__ == "__main__":
    main()