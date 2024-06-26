import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from traits import generate_random_traits, inherit_traits, apply_random_mutation, generate_random_name

class Cat(pygame.sprite.Sprite):
    def __init__(self, cat_images, shelters, traits=None, name=None):
        super().__init__()
        self.image = random.choice(cat_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.health = 100
        self.hunger = random.randint(0, 100)
        self.thirst = random.randint(0, 100)
        self.cleanliness = 100
        self.speed = random.uniform(1, 3)
        self.direction = random.choice(["left", "right", "up", "down"])
        self.move_counter = 0
        self.rest_counter = 0
        self.shelters = shelters

        self.target_food = None  # Initialize target_food attribute
        self.target_water = None  # Initialize target_water attribute
        self.target_cat = None  # Initialize target_cat attribute

        if traits is None:
            self.traits = generate_random_traits()
        else:
            self.traits = apply_random_mutation(traits)

        if name is None:
            self.name = generate_random_name()
        else:
            self.name = name

        self.fur_color = self.traits["fur_color"]
        self.eye_color = self.traits["eye_color"]
        self.behavior = self.traits["behavior"]
        self.personality = self.traits["personality"]
        self.breed = self.traits["breed"]

    def update(self, foods, waters, cats):
        self.hunger += 0.1
        self.thirst += 0.1
        if self.hunger > 70 and foods:
            self.target_food = min(foods, key=lambda food: self.distance_to(food.rect))
            self.move_towards(self.target_food.rect.x, self.target_food.rect.y)
        elif self.thirst > 70 and waters:
            self.target_water = min(waters, key=lambda water: self.distance_to(water.rect))
            self.move_towards(self.target_water.rect.x, self.target_water.rect.y)
        else:
            self.wander()
        self.check_interactions(foods, waters, cats)

    def distance_to(self, target_rect):
        dx = self.rect.centerx - target_rect.centerx
        dy = self.rect.centery - target_rect.centery
        return (dx ** 2 + dy ** 2) ** 0.5

    def check_interactions(self, foods, waters, cats):
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
        for cat in cats:
            if cat != self and self.rect.colliderect(cat.rect):
                self.interact_with_cat(cat)

    def interact_with_cat(self, other_cat):
        if self.personality == "Playful" and other_cat.personality in ["Playful", "Friendly"]:
            self.play_with(other_cat)
        elif self.personality == "Aggressive" or other_cat.personality == "Aggressive":
            self.fight_with(other_cat)
        elif self.personality == "Shy" and other_cat.personality == "Friendly":
            self.groom(other_cat)

    def play_with(self, other_cat):
        self.health = min(100, self.health + 10)
        other_cat.health = min(100, other_cat.health + 10)

    def fight_with(self, other_cat):
        self.health = max(0, self.health - 20)
        other_cat.health = max(0, other_cat.health - 20)

    def groom(self, other_cat):
        self.cleanliness = min(100, self.cleanliness + 10)
        other_cat.cleanliness = min(100, other_cat.cleanliness + 10)

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

            if self.behavior == "lazy":
                self.rest_counter = random.randint(50, 100)
            elif self.behavior == "active":
                self.rest_counter = random.randint(10, 20)
            elif self.behavior == "curious":
                self.rest_counter = random.randint(20, 40)
            elif self.behavior == "timid":
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
