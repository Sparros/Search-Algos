import pygame
import random

import Node
import Algos
import Menu
from Menu import Menu, NEW_MAZE_EVENT, START_EVENT, FREE_DRAW_EVENT

START_EVENT = pygame.USEREVENT + 1
NEW_MAZE_EVENT = pygame.USEREVENT + 2

# Initialize pygame
pygame.init()
pygame.display.set_caption("grid")


PADDING = 20
MENU_WIDTH = 250
WIDTH = 800 
HEIGHT = 800 
ROWS = 25
FONT_SIZE = 24

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
			node = Node.Node(i, j, gap, rows)
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
			node = Node.Node(source_grid[i][j].row, source_grid[i][j].col, source_grid[i][j].width, source_grid[i][j].total_rows)
			copied_grid[i].append(node)
			if source_grid[i][j].is_start():
				node.make_start()
			elif source_grid[i][j].is_end():
				node.make_end()
			elif source_grid[i][j].is_barrier():
				node.make_barrier()
	return copied_grid

# Draw the grid lines between the nodes
def draw_grid_lines(surface, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(surface, (128, 128, 128), (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(surface, (128, 128, 128), (j * gap, 0), (j * gap, width))

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

# Draw the grid
def draw(surface, grid, rows, width):
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

def free_draw(surface, grid, rows, width):
	if pygame.mouse.get_pressed()[0]: # LEFT
		pos = pygame.mouse.get_pos()
		row, col = get_clicked_pos(pos, ROWS, width)
		node = grid[row][col]
		if not start and node != end:
			start = node
			start.make_start()

		elif not end and node != start:
			end = node
			end.make_end()

		elif node != end and node != start:
			node.make_barrier()

	elif pygame.mouse.get_pressed()[2]: # RIGHT
		pos = pygame.mouse.get_pos()
		row, col = get_clicked_pos(pos, ROWS, width)
		node = grid[row][col]
		node.reset()
		if node == start:
			start = None
		elif node == end:
			end = None

def run_algorithms(algos_grids):
	for algo, surface, grid_pos, start_pos, end_pos in algos_grids:
		Algos.A_star(lambda: draw(surface, grid_pos, ROWS, GRID_WIDTH), grid_pos, start_pos, end_pos)
		Algos.DFS(lambda: draw(surface, grid_pos, ROWS, GRID_WIDTH), grid_pos, start_pos, end_pos)

def main():
	grid_needs_update = True
	while True:
		if grid_needs_update:
			top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, start_node, end_node = create_and_copy_grids(ROWS, GRID_WIDTH)
			grid_needs_update = False

		draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH)
		draw(top_right_surf, top_right_grid, ROWS, GRID_WIDTH)
		draw(bottom_left_surf, bottom_left_grid, ROWS, GRID_WIDTH)
		draw(bottom_right_surf, bottom_right_grid, ROWS, GRID_WIDTH)

		top_let_title = create_title_surface("A* Search")
		top_right_title = create_title_surface("DFS Search")
		bottom_left_title = create_title_surface("Bottom Left Grid")
		bottom_right_title = create_title_surface("Bottom Right Grid")
		# Blit the grid surfaces onto the window
		GRID_SCREEN.blit(top_let_title, (0, PADDING))
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
			menu.handle_event(event)
			if event.type == START_EVENT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
				grids = [top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid]
				for grid in grids:
					for row in grid:
						for node in row:
							node.update_neighbours(grid)
				run_algorithms([
					(Algos.A_star, top_left_surf, top_left_grid, start_node, end_node),
					(Algos.DFS, top_right_surf, top_right_grid, start_node, end_node),
					# Add more algorithms and grids here as needed
				])

			elif event.type == NEW_MAZE_EVENT:
				grid_needs_update = True
			
			elif event.type == FREE_DRAW_EVENT:
				free_draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH)
				free_draw(top_right_surf, top_right_grid, ROWS, GRID_WIDTH)
				free_draw(bottom_left_surf, bottom_left_grid, ROWS, GRID_WIDTH)
				free_draw(bottom_right_surf, bottom_right_grid, ROWS, GRID_WIDTH)

		# Update the menu and display
		menu.update(0.0)
		pygame.display.flip()

main()