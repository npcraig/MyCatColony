# ui.py
import pygame

def draw_button(screen, x, y, width, height, text, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def check_button_click(x, y, width, height, mouse_pos):
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        return True
    return False
