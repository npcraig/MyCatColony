# shelter.py
import pygame

class Shelter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([100, 100])
        self.image.fill((150, 75, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
