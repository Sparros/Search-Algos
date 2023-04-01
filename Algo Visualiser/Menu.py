import pygame_gui
import pygame
from pygame_gui.core import ObjectID

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.manager = pygame_gui.UIManager((width, height), 'Algo Visualiser\\themes.json')

        # Create menu elements
        self.title_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((10, 10), (self.width - 20, 24)),
            text='Algorithm Pathfinding',
            manager=self.manager,
            object_id="#menu-title"
        )
        button_width = 100
        button_height = 50
        gap = 10
        vertical_gap = 50

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 50), (button_width, button_height)),
            text='Start',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#start-button')
        )
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_width + gap + 10, 50), (button_width, button_height)),
            text='Restart',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#reset-button')
        )

        # column_names = ["Algorithm", "Time"]
        # row_data = [["A*", "BFS", "DFS", "Dijkstra"],[0, 0, 0, 0]]
        # # Create a UITable object
        # table_rect = pygame.Rect((10, 120), (self.width - 20, self.height - 130))
        # self.table = pygame_gui.elements.UITable(
        #     relative_rect=table_rect,
        #     data=row_data,
        #     column_titles=column_names,
        #     manager=self.manager,
        #     object_id=ObjectID(class_id='@table', 
        #                     object_id='#my-table')
        # )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((75, 450), (button_width, button_height)),
            text='New Maze',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#new-maze-button')
        )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((75, 450 + vertical_gap + button_height), (button_width, button_height)),
            text='Free Draw',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#free-draw-button')
        )

    def handle_event(self, event):
        # Handle GUI events
        self.manager.process_events(event)

        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_button:
                    # Start button clicked, do something
                    print('Start button clicked')
                # Add more button click handlers here

    def update(self, delta):
        # Update GUI
        self.manager.update(delta)

    def draw(self, surface):
        # Draw the menu to a surface
        surface.fill((29,34,40,255))
        self.manager.draw_ui(surface)
