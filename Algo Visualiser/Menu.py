import pygame_gui
import pygame
from pygame_gui.core import ObjectID

class Menu:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.manager = pygame_gui.UIManager((width, height), 'Algo Visualiser\\themes.json')
		self.create_table()

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

		self.restart_button = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((button_width + gap + 10, 50), (button_width, button_height)),
			text='Restart',
			manager=self.manager,
			object_id=ObjectID(class_id='@button', 
							   object_id='#reset-button')
		)

		self.new_maze_button = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((75, 450), (button_width, button_height)),
			text='New Maze',
			manager=self.manager,
			object_id=ObjectID(class_id='@button', 
							   object_id='#new-maze-button')
		)

		self.free_draw_button = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((75, 450 + vertical_gap + button_height), (button_width, button_height)),
			text='Free Draw',
			manager=self.manager,
			object_id=ObjectID(class_id='@button', 
							   object_id='#free-draw-button')
		)

		self.title_label = pygame_gui.elements.ui_label.UILabel(
					relative_rect=pygame.Rect((20, 310), (self.width - 20, 24)),
					text='Run algorithms:',
					manager=self.manager,
					object_id="#Algo-sequence-title"
				)
		# Create custom checkboxes
		self.sequential_checkbox = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((40, 340), (150, 30)),
			text='[ ] Sequential',
			manager=self.manager,
			object_id=ObjectID(class_id='@checkbox_button', 
		      					object_id='#sequential-check-box')
		)
		self.sequential_checkbox.checked = False

		self.parallel_checkbox = pygame_gui.elements.UIButton(
			relative_rect=pygame.Rect((40, 380), (150, 30)),
			text='[X] Parallel',
			manager=self.manager,
			object_id=ObjectID(class_id='@checkbox_button', 
		      					object_id='#parallel-check-box')
		)
		self.parallel_checkbox.checked = True

		self.title_label = pygame_gui.elements.ui_label.UILabel(
			relative_rect=pygame.Rect((20, 10), (self.width - 20, 24)),
			text='Simulate:',
			manager=self.manager,
			object_id="#simulate-title"
		)

		

	def create_table(self):
		column_names = ["Algorithm", "Time"]
		row_data = [["A*", "BFS", "DFS", "Dijkstra"], [0, 0, 0, 0]]
		pos = (30, 120)
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
				elif event.ui_element == self.new_maze_button:
					action = "NEW_MAZE_EVENT"				
				elif event.ui_element == self.free_draw_button:
					action = "FREE_DRAW_EVENT"
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
		return action
	
	def update(self, delta):
		# Update GUI
		self.manager.update(delta)

	def draw(self, surface):
		# Draw the menu to a surface
		surface.fill((29,34,40,255))
		self.manager.draw_ui(surface)
