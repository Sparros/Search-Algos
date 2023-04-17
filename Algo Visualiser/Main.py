import pygame
import random
from queue import PriorityQueue

import Node
import Algos
import Menu
from Menu import Menu

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

def create_single_grid(rows, width):
    gap = width // rows
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node.Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def create_and_copy_grids(rows, width, traffic):
    global FREE_DRAW_MODE
    base_grid = create_single_grid(rows, width)

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
def create_title_surface(title):
    font = pygame.font.SysFont(None, FONT_SIZE)
    text = font.render(title, True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (GRID_WIDTH // 2, FONT_SIZE // 2)
    surface = pygame.Surface((GRID_WIDTH, FONT_SIZE))
    surface.fill((255, 255, 255))
    surface.blit(text, text_rect)
    return surface

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

def free_draw(surface, grid, rows, width, start_end_nodes, x_offset, y_offset):
    start, end = start_end_nodes
    node = None

    if pygame.mouse.get_pressed()[0]:  # LEFT
        pos = pygame.mouse.get_pos()
        pos = (pos[0] - x_offset, pos[1] - y_offset) 
        row, col = get_clicked_pos(pos, rows, width)
        
        if 0 <= row < rows and 0 <= col < rows:
            node = grid[row][col]
            if not start:
                start = node
                start.make_start()
                start_end_nodes = (start, end)

            elif not end and node != start:
                end = node
                end.make_end()
                start_end_nodes = (start, end)

            elif node != end and node != start:
                node.make_barrier()

    elif pygame.mouse.get_pressed()[2]:  # RIGHT
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

    return start_end_nodes

def run_algorithms_sequentially(grids, start_node, end_node):
    print(f"Sequential - start node: {start_node}, end node: {end_node}")
    Algos.A_star(grids[0], start_node, end_node, (lambda node: node.draw(top_left_surf)), update_display)  
    Algos.DFS(grids[1], start_node, end_node, (lambda node: node.draw(top_right_surf)), update_display)
    Algos.BFS(grids[2], start_node, end_node, (lambda node: node.draw(bottom_left_surf)), update_display)
    Algos.dijkstra(grids[3], start_node, end_node, (lambda node: node.draw(bottom_right_surf)), update_display)


def run_algorithms_parallel(grids, start_node, end_node):
    print(f"Parallel - start node: {start_node}, end node: {end_node}")
    # Use threading to run algorithms in parallel
    from threading import Thread

    thread1 = Thread(target=Algos.A_star, args=(grids[0], start_node, end_node, (lambda node: node.draw(top_left_surf)), update_display))
    thread2 = Thread(target=Algos.DFS, args=(grids[1], start_node, end_node, (lambda node: node.draw(top_right_surf)), update_display))
    thread3 = Thread(target=Algos.BFS, args=(grids[2], start_node, end_node, (lambda node: node.draw(bottom_left_surf)), update_display))
    thread4 = Thread(target=Algos.dijkstra, args=(grids[3], start_node, end_node, (lambda node: node.draw(bottom_right_surf)), update_display))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

def update_grids(surfaces, grids, rows, width, start_end_nodes):
    if FREE_DRAW_MODE:      
        start_end_nodes = free_draw(top_left_surf, grids[0], ROWS, GRID_WIDTH, start_end_nodes, PADDING + MENU_WIDTH, PADDING + FONT_SIZE)
        start_node = start_end_nodes[0]
        end_node = start_end_nodes[1]
        return start_node, end_node
    else:
        start_node, end_node = set_start_end(grids[0], 1, 1, ROWS - 2, ROWS - 2)
    for surf, grid in zip(surfaces, grids):
        draw(surf, grid, rows, width)
    return start_node, end_node

def create_app():
    top_left_title = create_title_surface("A* Search")
    top_right_title = create_title_surface("DFS Search")
    bottom_left_title = create_title_surface("BFS Search")
    bottom_right_title = create_title_surface("Dijkstra Search")

    # Blit the grid surfaces onto the window
    GRID_SCREEN.blit(top_left_title, (PADDING, PADDING))
    GRID_SCREEN.blit(top_left_surf, (PADDING, PADDING + FONT_SIZE))
    GRID_SCREEN.blit(top_right_title, (GRID_WIDTH + PADDING * 3, PADDING))
    GRID_SCREEN.blit(top_right_surf, (GRID_WIDTH + PADDING * 3, PADDING + FONT_SIZE))
    GRID_SCREEN.blit(bottom_left_title, (PADDING, GRID_HEIGHT + PADDING * 2 + FONT_SIZE))
    GRID_SCREEN.blit(bottom_left_surf, (PADDING, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2))
    GRID_SCREEN.blit(bottom_right_title, (GRID_WIDTH + PADDING * 3, GRID_HEIGHT + PADDING * 2 + FONT_SIZE))
    GRID_SCREEN.blit(bottom_right_surf, (GRID_WIDTH + PADDING * 3, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2))
    WIN.blit(GRID_SCREEN, (MENU_WIDTH, 0))

    # Draw the menu
    WIN.blit(MENU, (0, 0))
    menu.draw(MENU)

    pygame.display.update()

def update_display():
    # Blit the grid surfaces onto the window
    GRID_SCREEN.blit(top_left_surf, (PADDING, PADDING + FONT_SIZE))
    GRID_SCREEN.blit(top_right_surf, (GRID_WIDTH + PADDING * 3, PADDING + FONT_SIZE))
    GRID_SCREEN.blit(bottom_left_surf, (PADDING, GRID_HEIGHT + PADDING * 3 + FONT_SIZE * 2))
    GRID_SCREEN.blit(bottom_right_surf, (GRID_WIDTH + PADDING * 3, GRID_HEIGHT + PADDING * 3 + FONT_SIZE * 2))
    WIN.blit(GRID_SCREEN, (MENU_WIDTH, 0))
    # Update the display
    pygame.display.flip()


def main():  
    global FREE_DRAW_MODE
    grid_needs_update = True
    execution_mode = "PARALLEL"
    start_end_nodes = (None, None)
    traffic = False
    global ROWS
    
    # initialise grids
    top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node = create_and_copy_grids(ROWS, GRID_WIDTH, traffic)

    surfaces = [top_left_surf, top_right_surf, bottom_left_surf, bottom_right_surf]
    grids = [top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid]

    while True:
        create_app()
        if grid_needs_update:
            start_node, end_node = update_grids(surfaces, grids, ROWS, GRID_WIDTH, start_end_nodes)
            grid_needs_update = False
        # if grid_needs_update: # if maze change or grid size change
        #     print("Updating grids")
        #     update_grids(surfaces, grids, ROWS, GRID_WIDTH)
        #     grid_needs_update = False
        #     start_node, end_node = set_start_end(top_left_grid, 1, 1, ROWS - 2, ROWS - 2)

        # if FREE_DRAW_MODE:
        #     start_end_nodes = free_draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH, start_end_nodes, PADDING + MENU_WIDTH, PADDING + FONT_SIZE)
        #     #update_grids(surfaces, grids, ROWS, GRID_WIDTH)

        # Handle events
        for event in pygame.event.get():
            action, traffic, new_rows = menu.handle_event(event)
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
                    run_algorithms_sequentially(grids, start_node, end_node)
                elif execution_mode == "PARALLEL":
                    run_algorithms_parallel(grids, start_node, end_node)
            
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
                FREE_DRAW_MODE = True
                if FREE_DRAW_MODE:
                    for grid in grids:
                        for row in grid: 
                            for node in row:
                                node.reset()

        # Update the menu and display
        menu.update(0.0)
        #pygame.display.update()

if __name__ == "__main__":
    main()