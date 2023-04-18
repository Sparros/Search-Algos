import pygame
from queue import PriorityQueue, Queue
from collections import deque
import heapq
import time
from Node import Node

TRAFFIC_COST = 2

def get_cost(node1, node2):
    if node1.is_traffic() or node2.is_traffic():
        return 2
    else:
        return 1

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, end, node_draw_func):
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = came_from.get(current)
        if current is not None:
            current.make_path()
            node_draw_func(current)
    path.reverse()
    return path

def A_star(grid, start, end, node_draw_func, update_display_func):
    # Start timer
    start_time = time.time()

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
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            # Calculate the path length
            path_length = len(path) - 1

            # Calculate the time taken
            time_taken = time.time() - start_time

            return (time_taken, path_length)
        
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

    return None, None, None

def DFS(grid, start, end, node_draw_func, update_display_func):
    start_time = time.time()
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
                path = reconstruct_path(came_from, end, node_draw_func)
                path_length = len(path) - 1
                time_taken = time.time() - start_time
                return (time_taken, path_length)

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

    return None, None, None

def BFS(grid, start, end, node_draw_func, update_display_func):
    start_time = time.time()
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
            path = reconstruct_path(came_from, end, node_draw_func)
            path_length = len(path) - 1
            time_taken = time.time() - start_time
            return (time_taken, path_length)

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

    return None, None, None

def dijkstra(grid, start, end, node_draw_func, update_display_func):
    start_time = time.time()
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
                if end not in came_from:
                        return False
                path = reconstruct_path(came_from, end, node_draw_func)
                path_length = len(path) - 1
                time_taken = time.time() - start_time
                end.make_end()
                return (time_taken, path_length)

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

def greedy_best_first(grid, start, end, node_draw_func, update_display_func):
    start_time = time.time()
    print("Greedy Best-First called")
    open_set = PriorityQueue()
    open_set.put((h(start.get_pos(), end.get_pos()), start))
    came_from = {}
    visited = set()

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]

        if current == end:
            path =reconstruct_path(came_from, end, node_draw_func)
            end.make_end()
            path_length = len(path) - 1
            time_taken = time.time() - start_time
            return (time_taken, path_length)

        visited.add(current)

        for neighbour in current.neighbours:
            if neighbour not in visited and not neighbour.is_barrier():
                came_from[neighbour] = current
                open_set.put((h(neighbour.get_pos(), end.get_pos()), neighbour))
                neighbour.make_open()
                node_draw_func(neighbour)
                update_display_func()

        if current != start:
            current.make_closed()
            node_draw_func(current)
            update_display_func()

    return False

def bidirectional_bfs(grid, start, end, node_draw_func, update_display_func):
    start_time = time.time()
    print("Bidirectional BFS called")
    start_queue = deque([start])
    end_queue = deque([end])
    start_visited = {start}
    end_visited = {end}
    came_from_start = {start: None}
    came_from_end = {end: None}

    while start_queue and end_queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_start = start_queue.popleft()
        current_end = end_queue.popleft()

        if current_start in end_visited or current_end in start_visited:
            path = []

            if current_start in end_visited:
                meet_point = current_start
            else:
                meet_point = current_end

            if meet_point in came_from_start and meet_point in came_from_end:
                while came_from_start[meet_point]:
                    meet_point = came_from_start[meet_point]
                    path.append(meet_point)
                path = path[::-1]
                while came_from_end[meet_point]:
                    meet_point = came_from_end[meet_point]
                    path.append(meet_point)

                for node in path:
                    node.make_path()
                    node_draw_func(node)
                update_display_func()
                end.make_end()

                path_length = len(path) - 1
                time_taken = time.time() - start_time
                return (time_taken, path_length)

        for neighbour in current_start.neighbours:
            if neighbour not in start_visited and not neighbour.is_barrier():
                start_visited.add(neighbour)
                came_from_start[neighbour] = current_start
                neighbour.make_open()
                node_draw_func(neighbour)
                start_queue.append(neighbour)
                update_display_func()

        for neighbour in current_end.neighbours:
            if neighbour not in end_visited and not neighbour.is_barrier():
                end_visited.add(neighbour)
                came_from_end[neighbour] = current_end
                neighbour.make_open()
                node_draw_func(neighbour)
                end_queue.append(neighbour)
                update_display_func()

        if current_start != start:
            current_start.make_closed()
            node_draw_func(current_start)
            update_display_func()

        if current_end != end:
            current_end.make_closed()
            node_draw_func(current_end)
            update_display_func()

    return False

def jps(grid, start, end, node_draw_func, update_display_func):
    print("JPS called")
    start.make_start()
    end.make_end()
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    h_score = {node: h(node.get_pos(), end.get_pos()) for row in grid for node in row}
    f_score = {node: g_score[node] + h_score[node] for row in grid for node in row}
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, node_draw_func)
            end.make_end()
            return True

        neighbors = []
        if current.parent is not None:
            neighbors = current.get_neighbors_with_parent()
        else:
            neighbors = current.get_all_neighbors()

        for neighbor in neighbors:
            if neighbor.is_closed() or neighbor.is_barrier():
                continue

            jump_node = jump(neighbor, current, end, grid)
            if jump_node is None:
                continue

            if jump_node in open_set_hash:
                new_g_score = g_score[current] + get_cost(current, jump_node)
                if new_g_score < g_score[jump_node]:
                    came_from[jump_node] = current
                    g_score[jump_node] = new_g_score
                    f_score[jump_node] = new_g_score + h_score[jump_node]
                    open_set.put((f_score[jump_node], jump_node))
            else:
                came_from[jump_node] = current
                g_score[jump_node] = g_score[current] + get_cost(current, jump_node)
                h_score[jump_node] = h(jump_node.get_pos(), end.get_pos())
                f_score[jump_node] = g_score[jump_node] + h_score[jump_node]
                open_set.put((f_score[jump_node], jump_node))
                open_set_hash.add(jump_node)
                jump_node.make_open()
                node_draw_func(jump_node)

        if current != start:
            current.make_closed()
            node_draw_func(current)
            update_display_func()

    return False
    
def jump(node, parent, end, grid):
    if node == end:
        return node

    x, y = node.get_pos()
    px, py = parent.get_pos()

    dx = x - px
    dy = y - py

    if dx != 0 and dy != 0:
        if (grid[x - dx][y + dy].is_barrier() and not grid[x - dx][y].is_barrier()) or (
                grid[x + dx][y - dy].is_barrier() and not grid[x][y - dy].is_barrier()):
            return node

    else:
        if dx != 0:
            if (grid[x + dx][y + 1].is_barrier() and not grid[x][y + 1].is_barrier()) or (
                    grid[x + dx][y - 1].is_barrier() and not grid[x][y - 1].is_barrier()):
                return node
        else:
            if (grid[x + 1][y + dy].is_barrier() and not grid[x + 1][y].is_barrier()) or (
                    grid[x - 1][y + dy].is_barrier() and not grid[x - 1][y].is_barrier()):
                return node

    if dx != 0 and dy != 0:
        if jump(grid[x + dx][y], node, end, grid) or jump(grid[x][y + dy], node, end, grid):
            return node

    elif dx != 0:
        if jump(grid[x + dx][y], node, end, grid):
            return node

    else:
        if jump(grid[x][y + dy], node, end, grid):
            return node

    return None

# def bellman_ford(grid, start, end, node_draw_func, update_display_func):
#     print("Bellman-Ford called")
#     came_from = {}
#     dist = {}
#     for row in grid:
#         for node in row:
#             if isinstance(node, Node):
#                 dist[node] = float("inf")
#     dist[start] = 0
    
#     for i in range(len(grid) * len(grid)):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
        
#         for row in grid:
#             for node in row:
#                 if isinstance(node, Node):
#                     for neighbour in node.neighbours:
#                         if not neighbour.is_barrier():
#                             if neighbour.is_traffic():
#                                 cost = 2
#                             else:
#                                 cost = 1
#                             if dist[node] + cost < dist[neighbour]:
#                                 dist[neighbour] = dist[node] + cost
#                                 came_from[neighbour] = node
#                                 neighbour.make_open()
#                                 node_draw_func(neighbour)
#                                 update_display_func()
#                                 if neighbour == end:
#                                     reconstruct_path(came_from, end, node_draw_func)
#                                     end.make_end()
#                                     return True

#         if i == len(grid) * len(grid) - 1:
#             print("Negative cycle detected")
#             return False
                                
#         if current != start:
#             current.make_closed()
#             node_draw_func(current)
#             update_display_func()

#     return False
