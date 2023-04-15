import pygame

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


class Node:
    def __init__(self, row, col, gap, total_rows):
        self.row = row
        self.col = col
        self.x = row * gap
        self.y = col * gap
        self.color = WHITE
        self.neighbours = []
        self.width = gap
        self.total_rows = total_rows
        self.distance = float("inf")

    def get_pos(self):
        return self.row, self.col
    
    def is_empty(self):
        return self.color == WHITE and not self.is_start() and not self.is_end()

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
    
    def is_traffic(self):
        return self.color == YELLOW

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

    def make_traffic(self):
        self.color = YELLOW

    def draw(self, win, offset_x=0, offset_y=0):
        pygame.draw.rect(win, self.color, pygame.Rect(self.x + offset_x, self.y + offset_y, self.width + 1, self.width + 1))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row + 1][self.col])
            #print(f"DOWN neighbor added: {grid[self.row + 1][self.col].get_pos()}")
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row - 1][self.col])
            #print(f"UP neighbor added: {grid[self.row - 1][self.col].get_pos()}")
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col + 1])
            #print(f"RIGHT neighbor added: {grid[self.row][self.col + 1].get_pos()}")
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col - 1])
            #print(f"LEFT neighbor added: {grid[self.row][self.col - 1].get_pos()}")

    def __lt__(self, other):
        return False
