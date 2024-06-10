# status_bar.py
import pygame

def draw_status_bar(screen, x, y, value, max_value, color, width=100, height=10):
    # Draw background bar
    pygame.draw.rect(screen, (200, 200, 200), (x, y, width, height))
    # Calculate width of the filled part
    filled_width = int(width * (value / max_value))
    # Draw filled part
    pygame.draw.rect(screen, color, (x, y, filled_width, height))
