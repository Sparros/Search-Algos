import pygame_gui
import pygame
from pygame_gui.core import ObjectID

# Define the algorithm list here
ALGO_LIST = ["A*", "BFS", "DFS", "Dijkstra", "Greedy Best-First", "Bidirectional BFS", "Jump Point Search", "Swarm Intelligence"]

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

        self.rows_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((self.width // 2 - 50, 400), (50, 24)),
            text="rows:",
            manager=self.manager,
        )
        self.row_drop_menu = pygame_gui.elements.UIDropDownMenu(
            relative_rect=pygame.Rect((self.width // 2 + 5, 400), (50, 24)),
            options_list=["10", "15", "20", "25", "30", "35", "40", "45", "50"],
            starting_option="25",
            manager=self.manager
        )

        self.title_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((20, 440), (self.width - 40, 24)),
            text='Simulate:',
            manager=self.manager,
            object_id="#simulate-title"
        )
        self.traffic_checkbox = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((30, 460), (self.width - 80, 30)),
            text='[ ] Traffic',
            manager=self.manager,
            object_id=ObjectID(class_id='@checkbox_button', 
                                object_id='#traffic-check-box')
        )
        self.traffic_checkbox.checked = False

        self.new_maze_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - button_width -5, 500), (button_width, button_height)),
            text='New Maze',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#new-maze-button')
        )
        self.regen_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((10, 500 + button_height), (self.width + 8, 28)),
            text='Maze requires regenerating',
            manager=self.manager,
            object_id=ObjectID(class_id='@regen-text', 
                               object_id='#regen-text')
        )
        self.regen_label.hide()

        self.free_draw_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 + 5, 500), (button_width, button_height)),
            text='Free Draw',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#free-draw-button')
        )

        checkbox_gap_x = 110
        checkbox_gap_y = 30
        max_width= 250
        max_height = 200

        self.checkboxes = []

        # Calculate the maximum number of rows and columns that can fit in the given max_width and max_height
        max_columns = max_width // checkbox_gap_x
        max_rows = max_height // checkbox_gap_y

        # Calculate the actual number of rows and columns based on the number of checkboxes
        if len(ALGO_LIST) <= max_columns:
            num_rows = 1
            num_columns = len(ALGO_LIST)
        else:
            num_rows = (len(ALGO_LIST) + max_columns - 1) // max_columns
            num_columns = max_columns

        # Calculate the actual width and height of the checkbox grid
        grid_width = num_columns * checkbox_gap_x
        grid_height = num_rows * checkbox_gap_y

        for i, algo in enumerate(ALGO_LIST):
            row = i // num_columns
            col = i % num_columns
            x_pos = (max_width - grid_width) // 2 + col * checkbox_gap_x
            y_pos = 570 + row * checkbox_gap_y
            checkbox = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x_pos, y_pos), (checkbox_gap_x, 30)),
                text=f"[{'X' if i < 4 else ' '}] {algo}",
                manager=self.manager,
                object_id=ObjectID(class_id='@checkbox_button', object_id=f'#algo-{i}-check-box')
            )
            checkbox.checked = True if i < 4 else False
            self.checkboxes.append(checkbox)

        self.user_help_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.width // 2 - button_width // 2, 700), (button_width, button_height)),
            text='Help',
            manager=self.manager,
            object_id=ObjectID(class_id='@button', 
                               object_id='#help-button')
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
        selected_algorithms = set(["A*", "BFS", "DFS", "Dijkstra"])
        # Handle GUI events
        self.manager.process_events(event)
        action = None
        rows = None
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
                        action = "SEQUENTIAL_EVENT"
                elif event.ui_element == self.parallel_checkbox:
                    if not self.parallel_checkbox.checked:
                        self.parallel_checkbox.checked = True
                        self.parallel_checkbox.set_text('[X] Parallel')
                        self.sequential_checkbox.checked = False
                        self.sequential_checkbox.set_text('[ ] Sequential')
                        action = "PARALLEL_EVENT"
                elif event.ui_element == self.traffic_checkbox:
                    if not self.traffic_checkbox.checked:
                        self.traffic_checkbox.checked = True
                        self.traffic_checkbox.set_text('[X] Traffic')
                        self.regen_label.show()
                    elif self.traffic_checkbox.checked:
                        self.traffic_checkbox.checked = False
                        self.traffic_checkbox.set_text('[ ] Traffic')
                        self.regen_label.hide()
                elif event.ui_element == self.new_maze_button:
                    action = "NEW_MAZE_EVENT"  
                    self.regen_label.hide()		
                    print("New maze button pressed")
                elif event.ui_element == self.free_draw_button:
                    action = "FREE_DRAW_EVENT"
                    print("Free draw button pressed")
                elif event.ui_element == self.user_help_button:
                    action = "HELP_EVENT"
                    
                # Handle algorithm checkboxes
                elif event.ui_element in self.checkboxes:
                    algo_index = self.checkboxes.index(event.ui_element)
                    algo_name = ALGO_LIST[algo_index]
                    if event.ui_element.checked:
                        if len(selected_algorithms) == 4:
                            event.ui_element.checked = False
                        else:
                            selected_algorithms.add(algo_name)
                    else:
                        selected_algorithms.discard(algo_name) # .remove causes KeyError if algo_name not in set

                    # Update the checkbox text
                    for i, checkbox in enumerate(self.checkboxes):
                        algo_name = ALGO_LIST[i]
                        checkbox.checked = algo_name in selected_algorithms
                        checkbox.set_text(f"[{'X' if algo_name in selected_algorithms else ' '}] {algo_name}")

            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    #if event.ui_element == self.row_drop_menu:
                    rows = int(event.text)  
                    action = "ROW_CHANGE_EVENT"

        return action, self.traffic_checkbox.checked, rows, selected_algorithms
    
    def update(self, delta):
        # Update GUI
        self.manager.update(delta)

    def draw(self, surface):
        # Draw the menu to a surface
        surface.fill((29,34,40,255))
        self.manager.draw_ui(surface)
