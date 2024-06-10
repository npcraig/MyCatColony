import pygame
import random

class Shelter(pygame.sprite.Sprite):
    def __init__(self, x, y, shelter_images):
        super().__init__()
        self.image = random.choice(shelter_images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
