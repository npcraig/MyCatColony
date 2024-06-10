import pygame

def draw_button(screen, rect, text, color, text_color):
    pygame.draw.rect(screen, color, rect)
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def check_button_click(rect, mouse_pos):
    return rect.collidepoint(mouse_pos)
