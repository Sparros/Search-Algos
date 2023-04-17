import tkinter as tk
from queue import PriorityQueue
import random
import pygame
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
ROWS = 50


class Node:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = 'white'
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == 'red'

	def is_open(self):
		return self.color == 'green'

	def is_barrier(self):
		return self.color == 'black'

	def is_start(self):
		return self.color == 'orange'

	def is_end(self):
		return self.color == 'turquoise'

	def reset(self):
		self.color = 'white'

	def make_start(self):
		self.color = 'orange'

	def make_closed(self):
		self.color = 'red'

	def make_open(self):
		self.color = 'green'

	def make_barrier(self):
		self.color = 'black'

	def make_end(self):
		self.color = 'turquoise'

	def make_path(self):
		self.color = 'purple'

	def draw(self):
		canvas.create_rectangle(self.x, self.y, self.x + self.width, self.y + self.width, fill=self.color)

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

def make_grid(rows, width):
	grid = []
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			node = Node(i, j, width, rows)
			grid[i].append(node)

	# Choose a random starting node
	current = random.choice(random.choice(grid))

	# Perform depth-first search to carve out a maze
	stack = [current]
	visited = set()
	while stack:
		current = stack.pop()
		if current not in visited:
			visited.add(current)
			neighbors = [n for n in current.neighbors if n not in visited]
			if neighbors:
				next_node = random.choice(neighbors)
				stack.append(current)
				remove_wall(current, next_node)
				current = next_node
	return grid

def remove_wall(current, next_node):
	x = current.row - next_node.row
	if x == 1:
		current.walls[0] = False
		next_node.walls[2] = False
	elif x == -1:
		current.walls[2] = False
		next_node.walls[0] = False

	y = current.col - next_node.col
	if y == 1:
		current.walls[3] = False
		next_node.walls[1] = False
	elif y == -1:
		current.walls[1] = False
		next_node.walls[3] = False

def draw_grid(grid):
	for row in grid:
		for node in row:
			node.draw()

def main():
	window = tk.Tk()
	window.title("A* Pathfinding Algorithm")

	grid = make_grid(ROWS, WINDOW_WIDTH // ROWS)

	start = None
	end = None

	while not start or not end:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					print("Space pressed")
					print(start.get_pos())
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

		draw(window, grid, ROWS, WINDOW_WIDTH)

	algorithm(lambda: draw(window, grid, ROWS, WINDOW_WIDTH), grid, start, end)

	pygame.quit()

if __name__ == '__main__':
	main()

window = tk.Tk()
window.title("Grid")
canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

grid = make_grid(ROWS, WINDOW_WIDTH)
draw_grid(grid)

window.mainloop()