import pygame

def draw_status_bar(screen, x, y, current, maximum, color, width=100, height=10):
    ratio = current / maximum
    pygame.draw.rect(screen, color, (x, y, width * ratio, height))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)
