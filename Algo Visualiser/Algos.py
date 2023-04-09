import pygame
from queue import PriorityQueue
from Node import Node

TRAFFIC_COST = 5

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
            if neighbour.is_traffic():
                temp_g_score += TRAFFIC_COST

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


