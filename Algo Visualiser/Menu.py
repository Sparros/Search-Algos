import pygame_gui
import pygame
from pygame_gui.core import ObjectID

class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.manager = pygame_gui.UIManager((width, height), 'Algo Visualiser\\themes.json')
        
        button_width = 100
        button_height = 50
        gap = 10
        vertical_gap = 50
        
        # Create menu elements: Height order
        self.title_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((10, 10), (self.width - 20, 24)),
            text='Algorithm Pathfinding',
            manager=self.manager,
            object_id="#menu-title"
        )
        
        # Start + Restart
        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - button_width -5, 50), (button_width, button_height)),
            text='Start',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#start-button')
        )
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 + 5, 50), (button_width, button_height)),
            text='Restart',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#reset-button')
        )

        self.create_table(30, 120)

        self.title_label = pygame_gui.elements.ui_label.UILabel(
                    relative_rect=pygame.Rect((20, 300), (self.width - 40, 24)),
                    text='Run algorithms:',
                    manager=self.manager,
                    object_id="#Algo-sequence-title"
                )
        self.sequential_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((40, 320), (self.width - 80, 30)),
            text='[ ] Sequential',
            manager=self.manager,
            object_id=ObjectID(class_id='@checkbox_button', 
                                  object_id='#sequential-check-box')
        )
        self.sequential_checkbox.checked = False
        self.parallel_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((40, 350), (self.width - 80, 30)),
            text='[X] Parallel',
            manager=self.manager,
            object_id=ObjectID(class_id='@checkbox_button', 
                                  object_id='#parallel-check-box')
        )
        self.parallel_checkbox.checked = True

        self.title_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((20, 420), (self.width - 40, 24)),
            text='Simulate:',
            manager=self.manager,
            object_id="#simulate-title"
        )
        self.traffic_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((40, 440), (self.width - 80, 30)),
            text='[ ] Traffic',
            manager=self.manager,
            object_id=ObjectID(class_id='@checkbox_button', 
                                object_id='#traffic-check-box')
        )
        self.traffic_checkbox.checked = False

        self.new_maze_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((75, 500), (button_width, button_height)),
            text='New Maze',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#new-maze-button')
        )

        self.free_draw_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((75, 520 + button_height), (button_width, button_height)),
            text='Free Draw',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#free-draw-button')
        )

    def create_table(self, pos_x, pos_y):
        column_names = ["Algorithm", "Time"]
        row_data = [["A*", "BFS", "DFS", "Dijkstra"], [0, 0, 0, 0]]
        pos = (pos_x, pos_y)
        cell_size = (100, 30)	
        
        num_columns = len(column_names)
        num_rows = len(row_data[0])

        # Create column headers
        for i, column_name in enumerate(column_names):
            header_label = pygame_gui.elements.ui_label.UILabel(
                relative_rect=pygame.Rect((pos[0] + i * cell_size[0], pos[1]), cell_size),
                text=column_name,
                manager=self.manager
            )

        # Create rows
        for i in range(num_rows):
            for j in range(num_columns):
                cell_label = pygame_gui.elements.ui_label.UILabel(
                    relative_rect=pygame.Rect((pos[0] + j * cell_size[0], pos[1] + (i + 1) * cell_size[1]), cell_size),
                    text=str(row_data[j][i]),
                    manager=self.manager
                )

    def handle_event(self, event):
        # Handle GUI events
        self.manager.process_events(event)
        action = None
        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:			
                if event.ui_element == self.start_button:                 
                    action = "START_EVENT"
                elif event.ui_element == self.sequential_checkbox:
                    if not self.sequential_checkbox.checked:
                        self.sequential_checkbox.checked = True
                        self.sequential_checkbox.set_text('[X] Sequential')
                        self.parallel_checkbox.checked = False
                        self.parallel_checkbox.set_text('[ ] Parallel')
                elif event.ui_element == self.parallel_checkbox:
                    if not self.parallel_checkbox.checked:
                        self.parallel_checkbox.checked = True
                        self.parallel_checkbox.set_text('[X] Parallel')
                        self.sequential_checkbox.checked = False
                        self.sequential_checkbox.set_text('[ ] Sequential')
                elif event.ui_element == self.traffic_checkbox:
                    if not self.traffic_checkbox.checked:
                        self.traffic_checkbox.checked = True
                        self.traffic_checkbox.set_text('[X] Traffic')
                    elif self.traffic_checkbox.checked:
                        self.traffic_checkbox.checked = False
                        self.traffic_checkbox.set_text('[ ] Traffic')
                elif event.ui_element == self.new_maze_button:
                    action = "NEW_MAZE_EVENT"				
                elif event.ui_element == self.free_draw_button:
                    action = "FREE_DRAW_EVENT"


        return action
    
    def update(self, delta):
        # Update GUI
        self.manager.update(delta)

    def draw(self, surface):
        # Draw the menu to a surface
        surface.fill((29,34,40,255))
        self.manager.draw_ui(surface)
