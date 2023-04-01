import pygame
import math
from queue import PriorityQueue
import random
import pygame_gui

import Node
import Algos
import Menu

# Initialize pygame
pygame.init()
pygame.display.set_caption("grid")


PADDING = 20
MENU_WIDTH = 250
WIDTH = 800 + (PADDING * 3)
HEIGHT = 800 + (PADDING * 3)
ROWS = 25
FONT_SIZE = 24

WIN = pygame.display.set_mode((MENU_WIDTH + WIDTH, HEIGHT))

MENU = pygame.Surface((MENU_WIDTH, HEIGHT))
menu = Menu.Menu(MENU_WIDTH, HEIGHT)

GRID = pygame.Surface((WIDTH, HEIGHT))
GRID.fill((255, 255, 255))

# Divide the grid into 4 rectangular areas
GRID_WIDTH = (WIDTH - PADDING * 3) // 2
GRID_HEIGHT = (HEIGHT - PADDING * 3) // 2

top_left_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
top_right_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
bottom_left_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))
bottom_right_surf = pygame.Surface((GRID_WIDTH, GRID_HEIGHT))

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

	return top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid

def draw_grid_lines(surface, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(surface, (128, 128, 128), (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(surface, (128, 128, 128), (j * gap, 0), (j * gap, width))

def draw(surface, grid, rows, width, title=None):
	surface.fill((255, 255, 255))
	if title:
		title_surf = create_title_surface(title)
		surface.blit(title_surf, (PADDING + (width - GRID_WIDTH) // 2, PADDING // 2))

	for row in grid:
		for node in row:
			node.draw(surface)

	draw_grid_lines(surface, rows, width)
	pygame.display.update()

def create_title_surface(title):
	font = pygame.font.SysFont(None, FONT_SIZE)
	text = font.render(title, True, (0, 0, 0))
	text_rect = text.get_rect()
	text_rect.center = (GRID_WIDTH // 2, FONT_SIZE // 2)
	surface = pygame.Surface((GRID_WIDTH, FONT_SIZE))
	surface.fill((255, 255, 255))
	surface.blit(text, text_rect)
	return surface

# Create the four lists of nodes
top_left_grid, top_right_grid, bottom_left_grid, bottom_right_grid = create_grids(ROWS, WIDTH // 2)

# Main loop
while True:
	# Handle events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			#sys.exit()
		# Handle menu events
		menu.handle_event(event)

	draw(top_left_surf, top_left_grid, ROWS, WIDTH // 2, "Top Left Grid")
	draw(top_right_surf, top_right_grid, ROWS, WIDTH // 2, "Top Right Grid")
	draw(bottom_left_surf, bottom_left_grid, ROWS, WIDTH // 2, "Bottom Left Grid")
	draw(bottom_right_surf, bottom_right_grid, ROWS, WIDTH // 2, "Bottom Right Grid")

	# Blit the grid surfaces onto the window
	GRID.blit(top_left_surf, (PADDING, PADDING))
	GRID.blit(top_right_surf, (GRID_WIDTH + PADDING * 2, PADDING))
	GRID.blit(bottom_left_surf, (PADDING, GRID_HEIGHT + PADDING * 2))
	GRID.blit(bottom_right_surf, (GRID_WIDTH + PADDING * 2, GRID_HEIGHT + PADDING * 2))
	WIN.blit(GRID, (MENU_WIDTH, 0))

	# Draw the menu 
	menu.draw(MENU)
	WIN.blit(MENU, (0, 0))
	
	# Update the menu and display
	menu.update(0.0)
	pygame.display.flip()
	