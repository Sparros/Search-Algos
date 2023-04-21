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
        self.colour = WHITE
        self.neighbours = []
        self.width = gap
        self.total_rows = total_rows
        self.distance = float("inf")
        self.parent = None # for JPS algo

    def set_parent(self, parent_node):
        self.parent = parent_node

    def get_pos(self):
        return self.row, self.col
    
    def is_empty(self):
        return self.colour == WHITE and not self.is_start() and not self.is_end()

    def is_closed(self):
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN

    def is_barrier(self):
        return self.colour == BLACK

    def is_start(self):
        return self.colour == ORANGE

    def is_end(self):
        return self.colour == TURQUOISE
    
    def is_traffic(self):
        return self.colour == YELLOW

    def reset(self):
        self.colour = WHITE

    def make_start(self):
        self.colour = ORANGE

    def make_closed(self):
        self.colour = RED

    def make_open(self):
        self.colour = GREEN

    def make_barrier(self):
        self.colour = BLACK

    def make_end(self):
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = PURPLE

    def make_traffic(self):
        self.colour = YELLOW
    
    def is_same_state(self, other):
        return self.colour == other.colour

    def draw(self, win, offset_x=0, offset_y=0):
        pygame.draw.rect(win, self.colour, pygame.Rect(self.x + offset_x, self.y + offset_y, self.width + 1, self.width + 1))

        # Always draw grid lines
        #pygame.draw.rect(win, GREY, (self.x, self.y, self.width, self.width), 1)

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

    def get_all_neighbours(self, grid):
        self.update_neighbours(grid)
        return self.neighbours
    
    def get_neighbours_with_parent(self, grid):
        if self.parent is None:
            return []

        px, py = self.parent.get_pos()
        x, y = self.get_pos()
        dx = x - px
        dy = y - py
        neighbours = []

        if abs(dx) == abs(dy):  # Diagonal movement
            if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
                neighbours.append(grid[self.row + 1][self.col])
            if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
                neighbours.append(grid[self.row - 1][self.col])
            if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
                neighbours.append(grid[self.row][self.col + 1])
            if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
                neighbours.append(grid[self.row][self.col - 1])
        else:  # Straight movement
            if dx != 0:  # Horizontal movement
                if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
                    neighbours.append(grid[self.row + 1][self.col])
                if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
                    neighbours.append(grid[self.row - 1][self.col])
            elif dy != 0:  # Vertical movement
                if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
                    neighbours.append(grid[self.row][self.col + 1])
                if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
                    neighbours.append(grid[self.row][self.col - 1])

        return neighbours
    
    def update_from(self, source_node):
        if source_node.is_barrier():
            self.make_barrier()
        elif source_node.is_start():
            self.make_start()
        elif source_node.is_end():
            self.make_end()
        elif source_node.is_traffic():
            self.make_traffic()
        else:
            self.reset()
    
    def __lt__(self, other):
        return False
