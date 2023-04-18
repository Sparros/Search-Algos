import pygame

# Initialize Pygame
pygame.init()

# Set the initial size of the window
width, height = 500, 500
screen = pygame.display.set_mode((width, height))

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Define the font to use for the text
font = pygame.font.SysFont(None, 24)

# Define the tab width and height
TAB_WIDTH = 100
TAB_HEIGHT = 50

# Define the number of tabs
num_tabs = 5
max_lines = 5
# Define the active tab index
active_tab_index = 0

# Define the tab titles and text
tab_titles = ["A* Search", "DFS Search", "BFS Search", "Dijkstra Search", "New Algorithm"]
tab_text = ["A* Search is a heuristic search algorithm that finds the shortest path between two points in a graph. It works by using a heuristic function to estimate the distance to the goal and exploring the most promising nodes first.",
            "DFS Search is a depth-first search algorithm that explores the depth of the search tree first. It can be used to find a path between two nodes in a graph, but it may not find the shortest path.",
            "BFS Search is a breadth-first search algorithm that explores the breadth of the search tree first. It can be used to find the shortest path between two nodes in a graph.",
            "Dijkstra Search is a shortest path algorithm that finds the shortest path between two points in a graph. It works by maintaining a list of the shortest paths to each node and updating the list as it explores the graph.",
            "This is a new algorithm that does amazing things. It is the best algorithm ever created."]

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Handle window resizing
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle tab clicks
            mouse_pos = pygame.mouse.get_pos()
            for i in range(num_tabs):
                if i != active_tab_index:
                    if i * TAB_WIDTH < mouse_pos[0] < (i + 1) * TAB_WIDTH and 0 < mouse_pos[1] < TAB_HEIGHT:
                        active_tab_index = i

    # Draw things to the screen
    screen.fill(WHITE)  # Fill the screen with white

    # Draw the tabs
    for i in range(num_tabs):
        if i == active_tab_index:
            pygame.draw.rect(screen, BLUE, (i * TAB_WIDTH, 0, TAB_WIDTH, TAB_HEIGHT))
        else:
            pygame.draw.rect(screen, GRAY, (i * TAB_WIDTH, 0, TAB_WIDTH, TAB_HEIGHT))
        tab_title = font.render(tab_titles[i], True, BLACK)
        screen.blit(tab_title, (i * TAB_WIDTH + 10, 10))

    # Draw the active tab text
    active_tab_lines = tab_text[active_tab_index].split("\n")
    active_tab_text = []
    for line in active_tab_lines:
        if font.size(line)[0] > width - 20:
            words = line.split(" ")
            new_line = ""
            for word in words:
                if font.size(new_line + " " + word)[0] < width - 20:
                    new_line += " " + word
                else:
                    active_tab_text.append(new_line.strip())
                    new_line = word
            active_tab_text.append(new_line.strip())
        else:
            active_tab_text.append(line)
    if len(active_tab_text_lines) > max_lines:
            active_tab_text_lines = active_tab_text_lines[:max_lines]
            active_tab_text_lines[-1] = active_tab_text_lines[-1][:-3] + "..."
    active_tab_text = "\n".join(active_tab_text_lines)
    active_tab_text_surf = font.render(active_tab_text, True, BLACK)
    active_tab_text_rect = active_tab_text_surf.get_rect()
    active_tab_text_rect.x = 10
    active_tab_text_rect.y = TAB_HEIGHT + 10
    screen.blit(active_tab_text_surf, active_tab_text_rect)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()