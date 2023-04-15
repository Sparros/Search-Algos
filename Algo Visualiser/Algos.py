import pygame
from queue import PriorityQueue, Queue
from collections import deque
import heapq
from Node import Node

TRAFFIC_COST = 5

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, node_draw_func):
    print("Reconstructing path")
    while current in came_from:
        current = came_from[current]
        if current is not None:
            current.make_path() 
            node_draw_func(current)


def A_star(grid, start, end, node_draw_func, update_display_func):
    print("A_star called")
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    #print(f"Start node: {start.get_pos()}")
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}
    #print(f"Open set initial: {open_set_hash}")
    #counter = 0
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        #print(f"Current node: {current.get_pos()}")  # Add this line
        #print(f"Open set size: {len(open_set_hash)}")  # Add this line

        if current == end:
            reconstruct_path(came_from, end, node_draw_func)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            #print(f"Neighbour: {neighbour.get_pos()}")
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
                    node_draw_func(neighbour)  
                    update_display_func() 
                     
       
        #counter += 1
        #print("loop count: ")
        #print(counter)
        if current != start:
            current.make_closed()
            node_draw_func(current)
            update_display_func()   

    return False

def DFS(grid, start, end, node_draw_func, update_display_func):
    stack = [start]
    visited = set()
    came_from = {}

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()
        if current not in visited:
            visited.add(current)

            if current == end:
                #print(came_from)
                reconstruct_path(came_from, end, node_draw_func)  # If you want to reconstruct the path, you can implement this.
                end.make_end()
                return True

            for neighbour in current.neighbours:
                if neighbour not in visited and not neighbour.is_barrier():
                    stack.append(neighbour)
                    came_from[neighbour] = current
                    neighbour.make_open()
                    node_draw_func(neighbour)
                    update_display_func()

            if current != start:
                current.make_closed()
                node_draw_func(current)
                update_display_func()

    return False

def BFS(grid, start, end, node_draw_func, update_display_func):
    visited = set()
    queue = Queue()
    queue.put(start)
    visited.add(start)
    came_from = {}
    
    while not queue.empty():
        current = queue.get()

        if current == end:
            reconstruct_path(came_from, end, node_draw_func)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            if neighbour not in visited:
                visited.add(neighbour)
                came_from[neighbour] = current
                queue.put(neighbour)
                neighbour.make_open()
                node_draw_func(neighbour)
                update_display_func()
                
        if current != start:
            current.make_closed()
            node_draw_func(current)
            update_display_func()

    return False

def dijkstra(grid, start, end, node_draw_func, update_display_func):
    pq = []
    heapq.heappush(pq, (0, start))
    came_from = dict()
    came_from[start] = None
    visited = set()

    for row in grid:
        for node in row:
            if isinstance(node, Node):
                node.distance = float("inf")

    start.distance = 0

    while len(pq) > 0:
        current = heapq.heappop(pq)[1]

        if current not in visited:
            visited.add(current)

            if current == end:
                if end in came_from:
                    reconstruct_path(came_from, end, node_draw_func)
                end.make_end()
                return True

            for neighbour in current.neighbours:
                temp_distance = current.distance + 1
                if temp_distance < neighbour.distance:
                    came_from[neighbour] = current
                    neighbour.distance = temp_distance
                    heapq.heappush(pq, (neighbour.distance, neighbour))
                    neighbour.make_open()
                    node_draw_func(neighbour)
                    update_display_func()

            if current != start:
                current.make_closed()
                node_draw_func(current)
                update_display_func()

    return False

