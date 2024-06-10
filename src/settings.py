import pygame

# Default Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BUTTON_COLOR = (100, 100, 200)
BUTTON_TEXT_COLOR = WHITE

# Initialize Pygame to get available resolutions
pygame.init()
available_resolutions = pygame.display.list_modes()

def set_resolution(width, height):
    global SCREEN_WIDTH, SCREEN_HEIGHT
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height

def get_available_resolutions():
    return available_resolutions
