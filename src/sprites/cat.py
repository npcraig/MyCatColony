import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Cat(pygame.sprite.Sprite):
    def __init__(self, cat_images, shelters):
        super().__init__()
        self.image = random.choice(cat_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.health = 100
        self.hunger = 0
        self.thirst = 0
        self.cleanliness = 100
        self.speed = random.uniform(1, 3)
        self.direction = random.choice(["left", "right", "up", "down"])
        self.move_counter = 0
        self.rest_counter = 0
        self.personality = random.choice(["active", "lazy", "curious", "timid"])
        self.shelters = shelters
        self.target_food = None
        self.target_water = None

    def update(self, foods, waters):
        if self.hunger > 70 and foods:
            self.target_food = min(foods, key=lambda food: self.rect.distance_to(food.rect))
            self.move_towards(self.target_food.rect.x, self.target_food.rect.y)
        elif self.thirst > 70 and waters:
            self.target_water = min(waters, key=lambda water: self.rect.distance_to(water.rect))
            self.move_towards(self.target_water.rect.x, self.target_water.rect.y)
        else:
            self.wander()
        self.check_interactions(foods, waters)

    def check_interactions(self, foods, waters):
        if self.target_food and self.rect.colliderect(self.target_food.rect):
            foods.remove(self.target_food)
            self.hunger = max(0, self.hunger - 40)
            self.target_food.kill()
            self.target_food = None
        if self.target_water and self.rect.colliderect(self.target_water.rect):
            waters.remove(self.target_water)
            self.thirst = max(0, self.thirst - 40)
            self.target_water.kill()
            self.target_water = None

    def feed(self, food):
        if food > 0:
            food -= 1
            self.hunger -= 20
            if self.hunger < 0:
                self.hunger = 0
        return food

    def give_water(self, water):
        if water > 0:
            water -= 1
            self.thirst -= 20
            if self.thirst < 0:
                self.thirst = 0
        return water

    def clean(self):
        self.cleanliness += 20
        if self.cleanliness > 100:
            self.cleanliness = 100

    def heal(self):
        self.health += 20
        if self.health > 100:
            self.health = 100

    def find_closest_shelter(self):
        min_dist = float('inf')
        closest_shelter = None
        for shelter in self.shelters:
            dist = ((self.rect.x - shelter.rect.x) ** 2 + (self.rect.y - shelter.rect.y) ** 2) ** 0.5
            if dist < min_dist:
                min_dist = dist
                closest_shelter = shelter
        return closest_shelter

    def move_towards(self, target_x, target_y):
        dx, dy = target_x - self.rect.x, target_y - self.rect.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def wander(self):
        if self.rest_counter > 0:
            self.rest_counter -= 1
            return

        if self.move_counter == 0:
            self.direction = random.choice(["left", "right", "up", "down"])
            self.move_counter = random.randint(30, 100)

            if self.personality == "lazy":
                self.rest_counter = random.randint(50, 100)
            elif self.personality == "active":
                self.rest_counter = random.randint(10, 20)
            elif self.personality == "curious":
                self.rest_counter = random.randint(20, 40)
            elif self.personality == "timid":
                self.rest_counter = random.randint(40, 60)
        else:
            self.move_counter -= 1
            if self.direction == "left":
                self.rect.x -= self.speed
                if self.rect.x < 0:
                    self.rect.x = SCREEN_WIDTH
            elif self.direction == "right":
                self.rect.x += self.speed
                if self.rect.x > SCREEN_WIDTH:
                    self.rect.x = 0
            elif self.direction == "up":
                self.rect.y -= self.speed
                if self.rect.y < 0:
                    self.rect.y = SCREEN_HEIGHT
            elif self.direction == "down":
                self.rect.y += self.speed
                if self.rect.y > SCREEN_HEIGHT:
                    self.rect.y = 0
