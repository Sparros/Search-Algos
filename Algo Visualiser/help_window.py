import os
import pygame
import pygame_gui
from PIL import Image

def load_gif(path):
    gif_frames = []
    gif = Image.open(path)

    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_surface = pygame.image.fromstring(
            gif.tobytes(), gif.size, gif.mode).convert()
        gif_frames.append(frame_surface)

    return gif_frames


def open_help_window():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Help")
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((800, 600), 'Algo Visualiser\\themes.json')

    algorithms = {
        "A*": "A* is a heuristic search algorithm that finds the shortest path between a start node and an end node. It uses a combination of the actual distance from the start node and an estimated distance to the end node (the heuristic) to decide which node to explore next. A* guarantees that it will find the shortest path if the heuristic is admissible (never overestimates the actual distance) and consistent (satisfies the triangle inequality).",
        "BFS": "Breadth-first search (BFS) is a graph traversal algorithm that explores all the vertices of a graph in breadthward motion. Starting from the source vertex, it explores all the vertices at the current depth before moving on to the vertices at the next depth. BFS is guaranteed to find the shortest path in an unweighted graph.",
        "DFS": "Depth-first search (DFS) is a graph traversal algorithm that explores as far as possible along each branch before backtracking. Starting from the source vertex, it explores one branch until it reaches the end, then backtracks and explores another branch. DFS is not guaranteed to find the shortest path and can get stuck in infinite loops if the graph has cycles.",
        "Dijkstra": "Dijkstra's algorithm is a shortest-path algorithm that finds the shortest path between a start node and all other nodes in a graph with non-negative edge weights. It works by maintaining a priority queue of nodes and their tentative distances from the start node, and repeatedly selecting the node with the smallest tentative distance and updating the distances of its neighbors. Dijkstra's algorithm guarantees that it will find the shortest path in a weighted graph with non-negative edge weights.",
        "Greedy Best-First": "Greedy best-first search is a heuristic search algorithm that always selects the node that appears to be closest to the goal. It uses an estimated distance to the goal (the heuristic) to decide which node to explore next. Greedy best-first search is not guaranteed to find the shortest path and can get stuck in local optima if the heuristic is not well-designed.",
        "Bidirectional BFS": "Bidirectional breadth-first search is a graph traversal algorithm that simultaneously searches from both the start node and the end node, and stops when the two searches meet in the middle. It uses two BFS searches, one starting from the source vertex and the other starting from the target vertex, to reduce the search space and improve efficiency. Bidirectional BFS is guaranteed to find the shortest path in an unweighted graph.",
        "Jump Point Search": "Jump point search is an optimization of A* for uniform-cost grid maps that reduces the number of nodes that need to be expanded by identifying 'jump points' that can be reached without intermediate expansions. It uses the same heuristic as A* but avoids exploring unnecessary nodes by jumping over large empty areas. Jump point search is guaranteed to find the shortest path in a uniform-cost grid map.",
        "Bellman-Ford": "Bellman-Ford algorithm is a single-source shortest path algorithm that finds the shortest path from a source node to all other nodes in a weighted graph. It works by first initializing the distance of the source node to itself as 0, and the distance to all other nodes as infinity. Then, it relaxes each edge in the graph n-1 times, where n is the total number of nodes in the graph. During each iteration, it considers all edges in the graph and updates the distance of each adjacent node if the distance through the current node is shorter than its current distance.\nThe algorithm uses a dynamic programming approach and iteratively improves the estimates of the shortest path until they converge to the optimal solution. In each iteration, the algorithm examines all edges in the graph and updates the distance to each node based on the minimum distance to its adjacent nodes. The key idea of the algorithm is the relaxation process, which involves checking whether the distance to a node can be improved by considering a path through a neighboring node.\nThe algorithm detects negative cycles in the graph by performing one additional iteration of the relaxation process. If any node's distance is updated during this iteration, it indicates that there exists a negative cycle in the graph. A negative cycle is a cycle in the graph whose total weight is negative, and it causes the algorithm to fail because it can lead to an infinitely decreasing distance.\nBellman-Ford algorithm has a time complexity of O(VE), where V is the number of nodes and E is the number of edges in the graph. This makes it less efficient than Dijkstra's algorithm, which has a time complexity of O((E+V)log V) for a binary heap implementation. However, unlike Dijkstra's algorithm, Bellman-Ford algorithm can handle graphs with negative edge weights."
    }

    # Create a selection list for the algorithm tabs
    algo_list = pygame_gui.elements.UISelectionList(
        relative_rect=pygame.Rect(0, 0, 200, 600),
        item_list=list(algorithms.keys()),
        manager=manager,
        object_id="#algo-tabs"
    )

    # Create a text box for displaying the algorithm information
    algo_textbox = pygame_gui.elements.UITextBox(
        html_text="<p>" + list(algorithms.values())[0] + "</p>",
        relative_rect=pygame.Rect(200, 0, 600, 600),
        manager=manager
    )

    bfs_gif_path = os.path.join("Algo Visualiser", "resources", "Breadth-First-Search-Algorithm", "Breadth-First-Search-Algorithm.gif")
    bfs_gif_frames = load_gif(bfs_gif_path)
    dfs_gif_path = os.path.join("Algo Visualiser", "resources", "Depth-First-Search", "Depth-First-Search.gif")
    dfs_gif_frames = load_gif(dfs_gif_path)

    # Scale down both GIFs
    scale_factor = 0.8
    bfs_gif_frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor))) for frame in bfs_gif_frames]
    dfs_gif_frames = [pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor))) for frame in dfs_gif_frames]

    # Remove the white background for both GIFs
    for frame in bfs_gif_frames:
        frame.set_colorkey((255, 255, 255))
    for frame in dfs_gif_frames:
        frame.set_colorkey((255, 255, 255))

    bfs_gif_index = 0
    bfs_gif_delay = 500
    bfs_gif_timer = 0
    dfs_gif_index = 0
    dfs_gif_delay = 500
    dfs_gif_timer = 0

    # Remove the white background
    for frame in bfs_gif_frames:
        frame.set_colorkey((255, 255, 255))

    # Calculate the position to center the GIF below the text
    gif_width, gif_height = bfs_gif_frames[0].get_size()
    gif_x = (200 + screen.get_width() - gif_width) // 2
    gif_y = (screen.get_height() - gif_height) // 2 + 100

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                    # Update the text box when a new algorithm is selected
                    selected_algo = algo_list.get_single_selection()
                    if selected_algo == "BFS":
                        bfs_gif_index = 0
                        bfs_gif_timer = -bfs_gif_delay
                        algo_textbox.set_text("<p>" + algorithms[selected_algo] + "</p>")
                    elif selected_algo == "DFS":
                        dfs_gif_index = 0
                        dfs_gif_timer = -dfs_gif_delay
                        algo_textbox.set_text("<p>" + algorithms[selected_algo] + "</p>")
                    else:
                        algo_textbox.set_text("<p>" + algorithms[selected_algo] + "</p>")

            manager.process_events(event)

        manager.update(time_delta)

        screen.fill((255, 255, 255))

        manager.draw_ui(screen)

        if algo_list.get_single_selection() == "BFS":
            current_time = pygame.time.get_ticks()
            if current_time - bfs_gif_timer > bfs_gif_delay:
                bfs_gif_index = (bfs_gif_index + 1) % len(bfs_gif_frames)
                bfs_gif_timer = current_time
            screen.blit(bfs_gif_frames[bfs_gif_index], (gif_x, gif_y))
        elif algo_list.get_single_selection() == "DFS":
            current_time = pygame.time.get_ticks()
            if current_time - dfs_gif_timer > dfs_gif_delay:
                dfs_gif_index = (dfs_gif_index + 1) % len(dfs_gif_frames)
                dfs_gif_timer = current_time
            screen.blit(dfs_gif_frames[dfs_gif_index], (gif_x, gif_y))
            
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    open_help_window()