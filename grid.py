import pygame
import math
from queue import PriorityQueue
import random

# Initialize pygame
pygame.init()

# Set up the window and left-hand menu sizes
GRID_WIDTH = 800
MENU_WIDTH = 200
WINDOW_HEIGHT = 800
MENU_HEIGHT = WINDOW_HEIGHT
FONT_SIZE = 24
#rows = 50

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

# Set up the window and left-hand menu surfaces
WINDOW = pygame.display.set_mode((GRID_WIDTH + MENU_WIDTH, WINDOW_HEIGHT))
GRID = pygame.Surface((GRID_WIDTH, WINDOW_HEIGHT))
MENU = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
MENU.fill((128, 128, 128))
pygame.display.set_caption("grid")

# Define the menu items and their positions
menu_items = [
	("Algorithm:", (10, 50)),
	("A*", (10, 100)),
	("Dijkstra", (10, 150)),
	("BFS", (10, 200)),
	("DFS", (10, 250))
]

# Set up the font for the menu items
font = pygame.font.Font(None, FONT_SIZE)

# Draw the menu items on the left-hand menu surface
for item in menu_items:
	text = font.render(item[0], True, WHITE)
	rect = text.get_rect()
	rect.topleft = item[1]
	MENU.blit(text, rect)

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
		pygame.draw.rect(GRID, self.color, (self.x, self.y, self.width, self.width))

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
def make_grid(rows, GRID_WIDTH):
	grid = []
	gap = GRID_WIDTH // rows
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
def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))
		
def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()

def main(win, width, rows):
	grid, start, end = make_grid(WINDOW_HEIGHT, GRID_WIDTH)
	running = True
	print(start, end)
	# Main loop
	while running:
		# Handle events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False

		# Draw the game grid
		for row in grid:
			for spot in row:
				spot.draw(win)
			
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, rows, width), grid, start, end)
		
		# Blit the left-hand menu onto the game window surface
		WINDOW.blit(MENU, (0, 0))
	
		# Update the display
		pygame.display.update()

	# Quit pygame
	pygame.quit()

main(WINDOW_HEIGHT, GRID_WIDTH, WINDOW_HEIGHT)