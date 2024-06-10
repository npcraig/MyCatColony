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

def load_and_resize_shelter(image_path, size):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, size)
    return image

def load_shelter_sprites(folder_path, sizes):
    sprites = []
    for i in range(1, len(sizes) + 1):
        image_path = f'{folder_path}/shelter_{i}.png'
        sprite = load_and_resize_shelter(image_path, sizes[i - 1])
        sprites.append(sprite)
    return sprites
