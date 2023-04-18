import pygame
import os
import sys
import pygame_gui

def open_help_window():
    print("Opening help window...")
    pygame.init()
    screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Help")
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((800, 600))

    algorithms = ["A*", "BFS", "DFS", "Dijkstra", "Greedy Best-First", "Bidirectional BFS", "Jump Point Search", "Swarm Intelligence"]

    # Create buttons for each algorithm
    buttons = {}
    for i, algo in enumerate(algorithms):
        buttons[algo] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(0, 75 * i, 150, 75),
                                                     text=algo,
                                                     manager=manager)

    # Create containers for each algorithm
    containers = {}
    for algo in algorithms:
        containers[algo] = pygame_gui.core.ui_container.UIContainer(relative_rect=pygame.Rect(150, 0, 650, 600),
                                                                     manager=manager)

        # Add your algorithm explanation text here
        algo_text = {
            "A*": "A* is a pathfinding algorithm that uses a combination of Dijkstra's algorithm and a heuristic function to estimate the remaining cost to the goal.",
            "BFS": "Breadth-First Search (BFS) is a graph traversal algorithm that explores all the vertices of a graph in breadthward motion, meaning it visits all neighbors of a vertex before visiting the neighbors' neighbors.",
            "DFS": "Depth-First Search (DFS) is a graph traversal algorithm that explores as far as possible along a branch before backtracking to explore other branches.",
            "Dijkstra": "Dijkstra's algorithm is a graph search algorithm that solves the single-source shortest path problem for a graph with non-negative edge weights, producing a shortest path tree.",
            "Greedy Best-First": "Greedy Best-First is a pathfinding algorithm that selects the node that appears to be closest to the goal using a heuristic function, without considering the cost to reach the current node.",
            "Bidirectional BFS": "Bidirectional BFS is a graph traversal algorithm that performs two simultaneous breadth-first searches, one from the start vertex and one from the end vertex, until the searches meet in the middle.",
            "Jump Point Search": "Jump Point Search is an optimization of A* algorithm for uniform-cost grid maps, which reduces the number of nodes that need to be expanded by identifying 'jump points' that can be reached without intermediate expansions.",
            "Swarm Intelligence": "Swarm Intelligence is a family of algorithms inspired by the collective behavior of decentralized, self-organized systems, such as ant colonies or flocks of birds. It can be applied to pathfinding problems by simulating the behavior of these systems."
        }[algo]

        pygame_gui.elements.UILabel(relative_rect=pygame.Rect(10, 10, 630, 220),
                                    text=algo_text,
                                    manager=manager,
                                    container=containers[algo])

        # Add example images and gifs for each algorithm
        # Replace 'path_to_image.png' and 'path_to_gif.gif' with the actual file paths for your images and gifs
        image_paths = {
            # "A*": "path_to_image.png",
            # "BFS": "path_to_image.png",
            # "DFS": "path_to_image.png",
            # "Dijkstra": "path_to_image.png",
            # "Greedy Best-First": "path_to_image.png",
            # "Bidirectional BFS": "path_to_image.png",
            # "Jump Point Search": "path_to_image.png",
            # "Swarm Intelligence": "path_to_image.png"
        }

        gif_paths = {
            # "A*": "path_to_gif.gif",
            "BFS": "Algo Visualiser/resources/Breadth-First-Search-Algorithm/Breadth-First-Search-Algorithm.gif",
            "DFS": "Algo Visualiser/resources/Depth-First-Search/Depth-First-Search.gif",
            # "Dijkstra": "path_to_gif.gif",
            # "Greedy Best-First": "path_to_gif.gif",
            # "Bidirectional BFS": "path_to_gif.gif",
            # "Jump Point Search": "path_to_gif.gif",
            # "Swarm Intelligence": "path_to_gif.gif"
        }

        images = {}
        for algo in algorithms:
            try:
                images[algo] = pygame.image.load(image_paths[algo]).convert_alpha()
                images[algo] = pygame.transform.scale(images[algo], (300, 200))
                screen.blit(images[algo], (350, 220))
                pygame.display.update()
            except KeyError:
                print(f"No image found for {algo}")

        gifs = {}
        for algo in algorithms:
            try:
                if algo in gif_paths:
                    gifs[algo] = pygame.image.load(gif_paths[algo]).convert_alpha()
                    gifs[algo] = pygame.transform.scale(gifs[algo], (300, 200))
                    screen.blit(gifs[algo], (350, 440))
                    pygame.display.update()
            except KeyError:
                print(f"No gif found for {algo}")

    # Hide the container if it's not the first algorithm
    for algo in algorithms[1:]:
        containers[algo].hide()

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                manager.resize_ui(event.w, event.h)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    for algo in algorithms:
                        if event.ui_element == buttons[algo]:
                            containers[algo].show()
                            screen.fill((0, 0, 0))  # Clear the screen
                            manager.draw_ui(screen)  # Draw UI elements
                            pygame.display.update()  # Update the display
                        else:
                            containers[algo].hide()

            manager.process_events(event)

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    open_help_window()