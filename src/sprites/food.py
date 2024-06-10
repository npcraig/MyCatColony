import pygame

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, food_image):
        super().__init__()
        self.image = food_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
