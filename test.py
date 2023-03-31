import pygame
import random


# Initialize Pygame
pygame.init()

# Set the width and height of the screen (width, height).
WINDOW_SIZE = (600, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set the title of the window
pygame.display.set_caption("Maze Solver")

# Set the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set the font
font = pygame.font.Font('freesansbold.ttf', 32)

# Set the cell size
CELL_SIZE = 30

def draw_grid(maze):
    """Draws the maze as a grid of cells."""
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            color = WHITE
            if maze[row][column] == 1:
                color = BLACK
            pygame.draw.rect(screen, color, [column * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE], 0)

def draw_path(path):
    """Draws the shortest path between the start and end points."""
    for cell in path:
        row = cell[0]
        col = cell[1]
        pygame.draw.rect(screen, BLUE, [col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE], 0)

def get_start_and_end(maze):
    """Returns the start and end points of the maze."""
    start = None
    end = None
    while start is None or end is None:
        row = random.randint(0, len(maze) - 1)
        col = random.randint(0, len(maze[0]) - 1)
        if maze[row][col] == 0:
            if start is None:
                start = (row, col)
                maze[row][col] = 2
            elif end is None and (row, col) != start:
                end = (row, col)
                maze[row][col] = 3
    return start, end

def solve_maze(maze):
    """Returns the shortest path between the start and end points."""
    start, end = get_start_and_end(maze)
    path = mazegenerator.find_path(maze, start, end)
    return path

def main():
    # Set the maze size
    maze_width = int(WINDOW_SIZE[0] / CELL_SIZE)
    maze_height = int(WINDOW_SIZE[1] / CELL_SIZE)

    # Generate the maze
    maze = mazegenerator.generate_maze(maze_width, maze_height)

    # Find the shortest path
    path = solve_maze(maze)

    # Draw the maze and path
    draw_grid(maze)
    draw_path(path)

    # Update the screen
    pygame.display.update()

    # Wait for spacebar to be pressed to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
