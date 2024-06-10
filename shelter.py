import pygame
import random
from sprite_loader import load_shelter_sprites

# Load and resize shelter images
shelter_sizes = [(100, 100), (150, 150), (200, 200)]  # Add more sizes as needed
shelter_images = load_shelter_sprites('assets', shelter_sizes)

class Shelter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(shelter_images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
