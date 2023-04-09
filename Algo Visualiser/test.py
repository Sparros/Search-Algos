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
WIDTH = 800 
HEIGHT = 800 
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
GRID_WIDTH = ((WIDTH - (PADDING * 3)) // 2) # Subtract the padding 3 times to have sapce either side and between the grids
GRID_HEIGHT = ((HEIGHT - (PADDING * 3) - (FONT_SIZE * 2)) // 2) # Subtract the font size  + Padding to make room for the text + padding

top_left_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
top_right_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
bottom_left_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
bottom_right_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))

import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, gap, total_rows):
        self.row = row
        self.col = col
        self.x = row * gap
        self.y = col * gap
        self.color = WHITE
        self.neighbours = []
        self.width = gap
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x, self.y, self.width + 1, self.width + 1))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
            print(f"DOWN neighbor added: {grid[self.row + 1][self.col].get_pos()}")
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])
            print(f"UP neighbor added: {grid[self.row - 1][self.col].get_pos()}")
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])
            print(f"RIGHT neighbor added: {grid[self.row][self.col + 1].get_pos()}")

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])
            print(f"LEFT neighbor added: {grid[self.row][self.col - 1].get_pos()}")

    def __lt__(self, other):
        return False

def generate_maze(grid, start, end):
    # Fill the grid with barriers
    for row in grid:
        for node in row:
            if not node.is_start() and not node.is_end():
                node.make_barrier()

    def get_neighbors(x, y):
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                neighbors.append((nx, ny, dx, dy))
        return neighbors

    def carve_paths(x, y, visited):
        visited.add((x, y))
        if not grid[x][y].is_start() and not grid[x][y].is_end():
            grid[x][y].reset()
        neighbors = get_neighbors(x, y)
        random.shuffle(neighbors)

        for nx, ny, dx, dy in neighbors:
            if (nx, ny) not in visited:
                grid[x + dx][y + dy].reset()
                carve_paths(nx, ny, visited)

    visited = set()
    carve_paths(start.row, start.col, visited)

def set_start_end(grid, start_row, start_col, end_row, end_col):
    start = grid[start_row][start_col]
    end = grid[end_row][end_col]
    start.make_start()
    end.make_end()
    return start, end

def create_single_grid(rows, width):
    gap = width // rows
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def create_and_copy_grids(rows, width):
    base_grid = create_single_grid(rows, width)
    start_node, end_node = set_start_end(base_grid, 1, 1, rows - 2, rows - 2)
    generate_maze(base_grid, start_node, end_node)
    
    top_left_grid = copy_grid(base_grid)
    top_right_grid = copy_grid(base_grid)
    bottom_left_grid = copy_grid(base_grid)
    bottom_right_grid = copy_grid(base_grid)

    return top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node

def copy_grid(source_grid):
    copied_grid = []
    for i in range(len(source_grid)):
        copied_grid.append([])
        for j in range(len(source_grid[i])):
            node = Node(source_grid[i][j].row, source_grid[i][j].col, source_grid[i][j].width, source_grid[i][j].total_rows)
            copied_grid[i].append(node)
            if source_grid[i][j].is_start():
                node.make_start()
            elif source_grid[i][j].is_end():
                node.make_end()
            elif source_grid[i][j].is_barrier():
                node.make_barrier()
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
    for i in range(rows):
        pygame.draw.line(surface, (128, 128, 128), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(surface, (128, 128, 128), (j * gap, 0), (j * gap, width))

# Draw the grid
def draw(surface, grid, rows, width):
    print("draw function called")
    surface.fill((255,255,255))
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

import pygame
from queue import PriorityQueue
from Node import Node

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def A_star(draw, grid, start, end):
    print("A_star called")
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        print(f"Current node: {current.get_pos()}")  # Add this line
        print(f"Open set size: {len(open_set_hash)}")  # Add this line

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            print(f"Neighbor: {neighbour.get_pos()}")
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw()
    
        if current != start:
            current.make_closed()

    return False

def DFS(draw, grid, start, end, visited=None):
    print("DFS called")
    if visited is None:
        visited = set()

    if start == end:
        print("Found end node")
        return True

    row, col = start.get_pos()
    neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    for neighbour_row, neighbour_col in neighbours:
        if 0 <= neighbour_row < len(grid) and 0 <= neighbour_col < len(grid[0]):
            neighbour = grid[neighbour_row][neighbour_col]
            if neighbour not in visited and not neighbour.is_barrier():
                visited.add(neighbour)
                neighbour.make_open()
                draw()

                if DFS(draw, grid, neighbour, end, visited):
                    print("Path found")
                    neighbour.make_path()
                    draw()
                    return True
                
                neighbour.make_closed()
                draw()
    print("DPS finished")
    return False


import pygame_gui
import pygame
from pygame_gui.core import ObjectID

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.manager = pygame_gui.UIManager((width, height), 'Algo Visualiser\\themes.json')
        
        button_width = 100
        button_height = 50
        gap = 10
        vertical_gap = 50
        
        # Create menu elements: Height order
        self.title_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((10, 10), (self.width - 20, 24)),
            text='Algorithm Pathfinding',
            manager=self.manager,
            object_id="#menu-title"
        )
        
        # Start + Restart
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - button_width -5, 50), (button_width, button_height)),
            text='Start',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#start-button')
        )
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 + 5, 50), (button_width, button_height)),
            text='Restart',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#reset-button')
        )

        self.create_table(30, 120)

        self.title_label = pygame_gui.elements.ui_label.UILabel(
                    relative_rect=pygame.Rect((20, 300), (self.width - 40, 24)),
                    text='Run algorithms:',
                    manager=self.manager,
                    object_id="#Algo-sequence-title"
                )
        self.sequential_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((40, 320), (self.width - 80, 30)),
            text='[ ] Sequential',
            manager=self.manager,
            object_id=ObjectID(class_id='@checkbox_button', 
                                  object_id='#sequential-check-box')
        )
        self.sequential_checkbox.checked = False
        self.parallel_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((40, 350), (self.width - 80, 30)),
            text='[X] Parallel',
            manager=self.manager,
            object_id=ObjectID(class_id='@checkbox_button', 
                                  object_id='#parallel-check-box')
        )
        self.parallel_checkbox.checked = True

        self.title_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((20, 420), (self.width - 40, 24)),
            text='Simulate:',
            manager=self.manager,
            object_id="#simulate-title"
        )
        self.traffic_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((40, 440), (self.width - 80, 30)),
            text='[ ] Traffic',
            manager=self.manager,
            object_id=ObjectID(class_id='@checkbox_button', 
                                object_id='#traffic-check-box')
        )
        self.traffic_checkbox.checked = False

        self.new_maze_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((75, 500), (button_width, button_height)),
            text='New Maze',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#new-maze-button')
        )

        self.free_draw_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((75, 520 + button_height), (button_width, button_height)),
            text='Free Draw',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#free-draw-button')
        )

    def create_table(self, pos_x, pos_y):
        column_names = ["Algorithm", "Time"]
        row_data = [["A*", "BFS", "DFS", "Dijkstra"], [0, 0, 0, 0]]
        pos = (pos_x, pos_y)
        cell_size = (100, 30)	
        
        num_columns = len(column_names)
        num_rows = len(row_data[0])

        # Create column headers
        for i, column_name in enumerate(column_names):
            header_label = pygame_gui.elements.ui_label.UILabel(
                relative_rect=pygame.Rect((pos[0] + i * cell_size[0], pos[1]), cell_size),
                text=column_name,
                manager=self.manager
            )

        # Create rows
        for i in range(num_rows):
            for j in range(num_columns):
                cell_label = pygame_gui.elements.ui_label.UILabel(
                    relative_rect=pygame.Rect((pos[0] + j * cell_size[0], pos[1] + (i + 1) * cell_size[1]), cell_size),
                    text=str(row_data[j][i]),
                    manager=self.manager
                )

    def handle_event(self, event):
        # Handle GUI events
        self.manager.process_events(event)
        action = None
        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:			
                if event.ui_element == self.start_button:                 
                    action = "START_EVENT"
                elif event.ui_element == self.sequential_checkbox:
                    if not self.sequential_checkbox.checked:
                        self.sequential_checkbox.checked = True
                        self.sequential_checkbox.set_text('[X] Sequential')
                        self.parallel_checkbox.checked = False
                        self.parallel_checkbox.set_text('[ ] Parallel')
                elif event.ui_element == self.parallel_checkbox:
                    if not self.parallel_checkbox.checked:
                        self.parallel_checkbox.checked = True
                        self.parallel_checkbox.set_text('[X] Parallel')
                        self.sequential_checkbox.checked = False
                        self.sequential_checkbox.set_text('[ ] Sequential')
                elif event.ui_element == self.traffic_checkbox:
                    if not self.traffic_checkbox.checked:
                        self.traffic_checkbox.checked = True
                        self.traffic_checkbox.set_text('[X] Traffic')
                    elif self.traffic_checkbox.checked:
                        self.traffic_checkbox.checked = False
                        self.traffic_checkbox.set_text('[ ] Traffic')
                elif event.ui_element == self.new_maze_button:
                    action = "NEW_MAZE_EVENT"				
                elif event.ui_element == self.free_draw_button:
                    action = "FREE_DRAW_EVENT"


        return action
    
    def update(self, delta):
        # Update GUI
        self.manager.update(delta)

    def draw(self, surface):
        # Draw the menu to a surface
        surface.fill((29,34,40,255))
        self.manager.draw_ui(surface)

def main():
    top_left_title = create_title_surface("A* Search")
    top_right_title = create_title_surface("DFS Search")
    bottom_left_title = create_title_surface("Bottom Left Grid")
    bottom_right_title = create_title_surface("Bottom Right Grid")
    
    global FREE_DRAW_MODE
    grid_needs_update = True
    start_end_nodes = (None, None)

    while True:
        if grid_needs_update:
            top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node = create_and_copy_grids(ROWS, GRID_WIDTH)
            draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH)
            draw(top_right_surf, top_right_grid, ROWS, GRID_WIDTH)
            draw(bottom_left_surf, bottom_left_grid, ROWS, GRID_WIDTH)
            draw(bottom_right_surf, bottom_right_grid, ROWS, GRID_WIDTH)
            grid_needs_update = False
        
        # Blit the grid surfaces onto the window
        GRID_SCREEN.blit(top_left_title, (0, PADDING))
        GRID_SCREEN.blit(top_left_surf, (PADDING, PADDING + FONT_SIZE))
        GRID_SCREEN.blit(top_right_title, (GRID_WIDTH + PADDING * 2, PADDING))
        GRID_SCREEN.blit(top_right_surf, (GRID_WIDTH + PADDING * 2, PADDING + FONT_SIZE))
        GRID_SCREEN.blit(bottom_left_title, (0, GRID_HEIGHT + PADDING * 2 + FONT_SIZE))
        GRID_SCREEN.blit(bottom_left_surf, (PADDING, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2))
        GRID_SCREEN.blit(bottom_right_title, (GRID_WIDTH + PADDING * 2, GRID_HEIGHT + PADDING * 2 + FONT_SIZE))
        GRID_SCREEN.blit(bottom_right_surf, (GRID_WIDTH + PADDING * 2, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2))
        WIN.blit(GRID_SCREEN, (MENU_WIDTH, 0))

        # Draw the menu
        WIN.blit(MENU, (0, 0))
        menu.draw(MENU)

        # Handle events
        for event in pygame.event.get():
            action = menu.handle_event(event)
            if action == "START_EVENT" or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                print("start event triggered")
                grids = [top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid]
                for grid in grids:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)       
                Algos.A_star(lambda: draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH), top_left_grid, start_node, end_node)   
                #Algos.DFS(lambda: None, top_right_grid, start_node, end_node)

            elif action == "NEW_MAZE_EVENT":
                grid_needs_update = True
            
            elif action == "FREE_DRAW_EVENT":
                FREE_DRAW_MODE = not FREE_DRAW_MODE
                if FREE_DRAW_MODE:
                    for grid in [top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid]:
                        for row in grid: 
                            for node in row:
                                node.reset()
        if FREE_DRAW_MODE:
            start_end_nodes = free_draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH, start_end_nodes, PADDING + MENU_WIDTH, PADDING + FONT_SIZE)
            # start_end_nodes = free_draw(top_right_surf, top_right_grid, ROWS,

            # start_end_nodes = free_draw(top_right_surf, top_right_grid, ROWS, GRID_WIDTH, start_end_nodes, GRID_WIDTH + PADDING * 2 + MENU_WIDTH, PADDING + FONT_SIZE)
            # start_end_nodes = free_draw(bottom_left_surf, bottom_left_grid, ROWS, GRID_WIDTH, start_end_nodes, PADDING + MENU_WIDTH, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2)
            # start_end_nodes = free_draw(bottom_right_surf, bottom_right_grid, ROWS, GRID_WIDTH, start_end_nodes, GRID_WIDTH + PADDING * 2 + MENU_WIDTH, GRID_HEIGHT + PADDING * 2 + FONT_SIZE * 2)

        # Update the menu and display
        menu.update(0.0)
        pygame.display.update()

main()