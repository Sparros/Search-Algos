import pygame
from queue import PriorityQueue

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
	print("A_star function called.")
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

def DFS(draw, grid, start, end, visited=None):
    if visited is None:
        visited = set()

    if start == end:
        return True

    row, col = start.get_pos()
    neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]

    for neighbor_row, neighbor_col in neighbors:
        if 0 <= neighbor_row < len(grid) and 0 <= neighbor_col < len(grid[0]):
            neighbor = grid[neighbor_row][neighbor_col]
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                neighbor.make_open()
                draw()

                if DFS(draw, grid, neighbor, end, visited):
                    neighbor.make_path()
                    draw()
                    return True

                neighbor.make_closed()
                draw()

    return False


