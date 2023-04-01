import pygame
import random

import Node
import Algos
import Menu

# Initialize pygame
pygame.init()
pygame.display.set_caption("grid")

PADDING = 20
MENU_WIDTH = 250
WIDTH = 800 
HEIGHT = 800 
ROWS = 20
FONT_SIZE = 24

WIN = pygame.display.set_mode((MENU_WIDTH + WIDTH, HEIGHT))

MENU = pygame.Surface((MENU_WIDTH, HEIGHT))
menu = Menu.Menu(MENU_WIDTH, HEIGHT)

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
	def is_valid(x, y):
		return 0 <= x < len(grid) and 0 <= y < len(grid[0])

	def get_neighbors(x, y):
		neighbors = []
		directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		for dx, dy in directions:
			nx, ny = x + dx * 2, y + dy * 2
			if is_valid(nx, ny):
				neighbors.append((nx, ny, dx, dy))
		return neighbors

	visited = set()
	start_pos = (start.row, start.col)
	end_pos = (end.row, end.col)
	visited.add(start_pos)
	visited.add(end_pos)
	frontier = [start_pos]

	while frontier:
		x, y = random.choice(frontier)
		if (x, y) != start_pos and (x, y) != end_pos: 
			grid[x][y].make_barrier()
		neighbors = get_neighbors(x, y)
		random.shuffle(neighbors)

		for nx, ny, dx, dy in neighbors:
			if (nx, ny) not in visited:
				visited.add((nx, ny))
				grid[x + dx][y + dy].make_barrier()
				frontier.append((nx, ny))

		frontier.remove((x, y))

	grid[start.row][start.col].reset()
	grid[end.row][end.col].reset()
	
# Create 4, 2D lists of nodes
def create_grids(rows, width):
	# Calculate the gap between nodes
	gap = width // rows

	# Create 4 grids of nodes
	top_left_grid = []
	for i in range(rows):
		top_left_grid.append([])
		for j in range(rows):
			node = Node.Node(i, j, gap, rows)
			top_left_grid[i].append(node)

	top_right_grid = []
	for i in range(rows):
		top_right_grid.append([])
		for j in range(rows):
			node = Node.Node(i, j, gap, rows)
			top_right_grid[i].append(node)

	bottom_left_grid = []
	for i in range(rows):
		bottom_left_grid.append([])
		for j in range(rows):
			node = Node.Node(i, j, gap, rows)
			bottom_left_grid[i].append(node)

	bottom_right_grid = []
	for i in range(rows):
		bottom_right_grid.append([])
		for j in range(rows):
			node = Node.Node(i, j, gap, rows)
			bottom_right_grid[i].append(node)

	# Set the start and end points
	top_left_start = top_left_grid[1][1]
	top_left_end = top_left_grid[rows - 2][rows - 2]
	top_left_start.make_start()
	top_left_end.make_end()

	# Add some randomly generated barriers to each grid
	generate_maze(top_left_grid, top_left_start, top_left_end)

	# Reset the start and end points after generating the maze
	top_left_start.make_start()
	top_left_end.make_end()

	return top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, top_left_start, top_left_end

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
def draw(surface, grid, rows, width, title=None):
	for row in grid:
		for node in row:
			node.draw(surface)
	
	draw_grid_lines(surface, rows, width)
	pygame.display.update()

# Create the four lists of nodes
top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid, top_left_start, top_left_end = create_grids(ROWS, GRID_WIDTH)

top_right_grid = copy_grid(top_left_grid)
bottom_left_grid = copy_grid(top_left_grid)
bottom_right_grid = copy_grid(top_left_grid)

# Main loop
while True:
	draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH)
	draw(top_right_surf, top_right_grid, ROWS, GRID_WIDTH)
	draw(bottom_left_surf, bottom_left_grid, ROWS, GRID_WIDTH)
	draw(bottom_right_surf, bottom_right_grid, ROWS, GRID_WIDTH)

	top_let_title = create_title_surface("Top Left Grid")
	top_right_title = create_title_surface("Top Right Grid")
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
	menu.draw(MENU)
	WIN.blit(MENU, (0, 0))

	# Handle events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			#sys.exit()
		# Handle menu events
		menu.handle_event(event)

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				# Run A* algorithm on the top-left grid
				Algos.A_star(lambda: draw(top_left_surf, top_left_grid, ROWS, GRID_WIDTH),  top_left_grid, top_left_start, top_left_end)
	
	# Update the menu and display
	menu.update(0.0)
	pygame.display.flip()
	