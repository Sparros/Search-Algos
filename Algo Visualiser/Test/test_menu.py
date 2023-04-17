import sys
import os
import pygame
import pygame_gui
import pytest
current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)
from Menu import Menu

@pytest.fixture
def menu():
    pygame.init()
    pygame_gui.core.ObjectID._id_counts = {}
    width = 200
    height = 800
    screen = pygame.display.set_mode((width, height))
    menu = Menu(width, height)
    yield menu
    pygame.quit()

def test_initialization(menu):
    assert menu.width == 200
    assert menu.height == 800
    assert isinstance(menu.manager, pygame_gui.UIManager)

def test_button_labels(menu):
    assert menu.start_button.text == "Start"
    assert menu.restart_button.text == "Restart"
    assert menu.sequential_checkbox.text == "[ ] Sequential"
    assert menu.parallel_checkbox.text == "[X] Parallel"
    assert menu.traffic_checkbox.text == "[ ] Traffic"
    assert menu.new_maze_button.text == "New Maze"
    assert menu.free_draw_button.text == "Free Draw"

def test_checkbox_initial_state(menu):
    assert not menu.sequential_checkbox.checked
    assert menu.parallel_checkbox.checked
    assert not menu.traffic_checkbox.checked

def test_handle_event_start_button(menu):
    event = pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_BUTTON_PRESSED, ui_element=menu.start_button)
    action, traffic_checked, rows = menu.handle_event(event)
    assert action == "START_EVENT"

def test_handle_event_sequential_checkbox(menu):
    event = pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_BUTTON_PRESSED, ui_element=menu.sequential_checkbox)
    action, traffic_checked, rows = menu.handle_event(event)
    assert action == "SEQUENTIAL_EVENT"
    assert menu.sequential_checkbox.checked
    assert not menu.parallel_checkbox.checked

def test_handle_event_parallel_checkbox(menu):
    # First, set sequential_checkbox.checked to True
    menu.sequential_checkbox.checked = True
    menu.parallel_checkbox.checked = False

    event = pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_BUTTON_PRESSED, ui_element=menu.parallel_checkbox)
    action, traffic_checked, rows = menu.handle_event(event)
    assert action == "PARALLEL_EVENT"
    assert not menu.sequential_checkbox.checked
    assert menu.parallel_checkbox.checked

def test_handle_event_traffic_checkbox(menu):
    event = pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_BUTTON_PRESSED, ui_element=menu.traffic_checkbox)
    action, traffic_checked, rows = menu.handle_event(event)
    assert action is None
    assert menu.traffic_checkbox.checked
    assert menu.regen_label.visible

def test_handle_event_new_maze_button(menu):
    event = pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_BUTTON_PRESSED, ui_element=menu.new_maze_button)
    action, traffic_checked, rows = menu.handle_event(event)
    assert action == "NEW_MAZE_EVENT"
    assert not menu.regen_label.visible

def test_handle_event_free_draw_button(menu):
    event = pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_BUTTON_PRESSED, ui_element=menu.free_draw_button)
    action, traffic_checked, rows = menu.handle_event(event)
    assert action == "FREE_DRAW_EVENT"

def test_handle_event_row_drop_menu(menu):
    event = pygame.event.Event(pygame.USEREVENT, user_type=pygame_gui.UI_DROP_DOWN_MENU_CHANGED, ui_element=menu.row_drop_menu, text="35")
    action, traffic_checked, rows = menu.handle_event(event)
    assert action == "ROW_CHANGE_EVENT"
    assert rows == 35

