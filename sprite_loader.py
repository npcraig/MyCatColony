import pygame

def load_and_resize_sprite(image_path, size):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, size)
    return image

def load_cat_sprites(folder_path, size):
    sprites = []
    for i in range(1, 11):
        image_path = f'{folder_path}/cat_{i}.png'
        sprite = load_and_resize_sprite(image_path, size)
        sprites.append(sprite)
    return sprites
