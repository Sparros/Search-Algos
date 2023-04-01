import pygame
import math
from queue import PriorityQueue
import random
import pygame_gui

# Initialize pygame
pygame.init()

MENU_WIDTH = 250
WIDTH = 800
ROWS = 50
FONT_SIZE = 24
WIN = pygame.display.set_mode((MENU_WIDTH + WIDTH, WIDTH))
MENU = pygame.Surface((MENU_WIDTH, WIDTH))
GRID = pygame.Surface((WIDTH, WIDTH))
pygame.display.set_caption("grid")
manager = pygame_gui.UIManager((MENU_WIDTH + WIDTH, WIDTH))

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

# Set up the font for the menu items
font = pygame.font.Font(None, FONT_SIZE)


class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
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
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False

def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False

def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()

# Create a 2D list of Spot objects
def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	# Add some randomly generated barriers
	for i in range(rows*2):
		row = random.randint(0, rows-1)
		col = random.randint(0, rows-1)
		spot = grid[row][col]
		spot.make_barrier()

	# Choose a random start and end point
	start = grid[random.randint(0, rows-1)][random.randint(0, rows-1)]
	end = grid[random.randint(0, rows-1)][random.randint(0, rows-1)]
	while end == start:
		end = grid[random.randint(0, rows-1)][random.randint(0, rows-1)]

	start.make_start()
	end.make_end()

	return grid, start, end

# Draw the grid on the screen
def draw_grid(grid, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(grid, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(grid, GREY, (j * gap, 0), (j * gap, width))
		
def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(GRID, rows, width)
	pygame.display.update()

def draw_menu():
	MENU.fill((29,34,40,255))
	
	# Draw the menu surface on the main window
	WIN.blit(MENU, (0, 0))
	# Update the display to show the menu
	pygame.display.update()

	

def main(win, width, rows):
	grid, start, end = make_grid(rows, width)
	run = True
	# Main loop
	while run:
		# Blit the left-hand menu onto the game window surface
		draw_menu()

		draw_grid(GRID,ROWS,WIDTH)
		# Draw the grid
		# draw(win, grid, ROWS, width)
		# for event in pygame.event.get():
		# 	if event.type == pygame.QUIT:
		# 		run = False
		# 	if event.type == pygame.KEYDOWN:
		# 		if event.key == pygame.K_SPACE:
		# 			print("Space pressed")
		# 			print(start.get_pos())
		# 			for row in grid:
		# 				for spot in row:
		# 					spot.update_neighbors(grid)

		# 			algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

		# Blit the grid surface to the window surface
		WIN.blit(GRID, (MENU_WIDTH, 0))

	# Quit pygame
	pygame.quit()

main(WIN, WIDTH, ROWS)