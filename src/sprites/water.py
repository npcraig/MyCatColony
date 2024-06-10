import pygame

class Water(pygame.sprite.Sprite):
    def __init__(self, x, y, water_image):
        super().__init__()
        self.image = water_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
