import pygame
import random
from status_bar import draw_status_bar
from ui import draw_button, check_button_click
from shelter import Shelter
from random_events import generate_random_event, handle_random_event
from sprite_loader import load_cat_sprites

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (100, 100, 200)
BUTTON_TEXT_COLOR = WHITE

# Load and resize cat images
cat_size = (50, 50)  # Desired size for cat sprites
cat_images = load_cat_sprites('assets', cat_size)

# Resource management
food = 100
water = 100
currency = 100  # New currency system

# Weather system
weather = "Sunny"
weather_effects = {
    "Sunny": {"hunger": 0.01, "thirst": 0.01},
    "Rainy": {"hunger": 0.02, "thirst": 0.01},
    "Windy": {"hunger": 0.01, "thirst": 0.02},
    "Snowy": {"hunger": 0.03, "thirst": 0.02}
}

# Day-night cycle
time_of_day = 0  # 0 to 2399, where 0-1199 is day and 1200-2399 is night
day_length = 2400  # Total number of ticks in a day

# Cat sprite
class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(cat_images)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.health = 100
        self.hunger = 0
        self.thirst = 0
        self.cleanliness = 100

    def update(self):
        global weather
        global time_of_day
        # Behavior affected by weather and time of day
        hunger_rate = weather_effects[weather]["hunger"]
        thirst_rate = weather_effects[weather]["thirst"]

        if 1200 <= time_of_day < 2400:  # Night time
            hunger_rate *= 0.5
            thirst_rate *= 0.5

        self.hunger += hunger_rate
        self.thirst += thirst_rate
        self.cleanliness -= 0.01
        if self.hunger > 100: self.hunger = 100
        if self.thirst > 100: self.thirst = 100
        if self.cleanliness < 0: self.cleanliness = 0

        # Decrease health if hunger, thirst, or cleanliness is too low
        if self.hunger >= 100 or self.thirst >= 100 or self.cleanliness <= 0:
            self.health -= 0.1
        if self.health < 0: self.health = 0

        # Seek shelter if hungry or thirsty
        if self.hunger > 80 or self.thirst > 80:
            closest_shelter = self.find_closest_shelter()
            if closest_shelter:
                self.move_towards(closest_shelter.rect.x, closest_shelter.rect.y)

    def feed(self):
        global food
        if food > 0:
            food -= 1
            self.hunger -= 20
            if self.hunger < 0: self.hunger = 0

    def give_water(self):
        global water
        if water > 0:
            water -= 1
            self.thirst -= 20
            if self.thirst < 0: self.thirst = 0

    def clean(self):
        self.cleanliness += 20
        if self.cleanliness > 100: self.cleanliness = 100

    def heal(self):
        self.health += 20
        if self.health > 100: self.health = 100

    def find_closest_shelter(self):
        min_dist = float('inf')
        closest_shelter = None
        for shelter in shelters:
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
            self.rect.x += dx * 2  # Move speed
            self.rect.y += dy * 2

# Helper function to create a new cat
def create_new_cat():
    new_cat = Cat()
    all_sprites.add(new_cat)
    cats.add(new_cat)

# Initialize the game window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Cat Colony Simulator")

# Sprite groups
all_sprites = pygame.sprite.Group()
cats = pygame.sprite.Group()
shelters = pygame.sprite.Group()

# Create multiple cats
for _ in range(5):
    cat = Cat()
    all_sprites.add(cat)
    cats.add(cat)

# Main game loop
running = True
clock = pygame.time.Clock()

# UI positions
feed_button_rect = pygame.Rect(20, 20, 200, 60)
water_button_rect = pygame.Rect(240, 20, 200, 60)
shelter_button_rect = pygame.Rect(460, 20, 200, 60)
clean_button_rect = pygame.Rect(680, 20, 200, 60)
heal_button_rect = pygame.Rect(900, 20, 200, 60)
buy_food_button_rect = pygame.Rect(20, 100, 200, 60)
buy_water_button_rect = pygame.Rect(240, 100, 200, 60)
gather_resources_button_rect = pygame.Rect(460, 100, 200, 60)
earn_money_button_rect = pygame.Rect(680, 100, 200, 60)  # New button for earning money

# Random event timer
event_timer = 0
event_interval = 5000  # 5 seconds
event_message = ""

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if check_button_click(feed_button_rect.x, feed_button_rect.y, feed_button_rect.width, feed_button_rect.height, mouse_pos):
                for cat in cats:
                    cat.feed()
            elif check_button_click(water_button_rect.x, water_button_rect.y, water_button_rect.width, water_button_rect.height, mouse_pos):
                for cat in cats:
                    cat.give_water()
            elif check_button_click(shelter_button_rect.x, shelter_button_rect.y, shelter_button_rect.width, shelter_button_rect.height, mouse_pos):
                x, y = random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100)
                shelter = Shelter(x, y)
                all_sprites.add(shelter)
                shelters.add(shelter)
            elif check_button_click(clean_button_rect.x, clean_button_rect.y, clean_button_rect.width, clean_button_rect.height, mouse_pos):
                for cat in cats:
                    cat.clean()
            elif check_button_click(heal_button_rect.x, heal_button_rect.y, heal_button_rect.width, heal_button_rect.height, mouse_pos):
                for cat in cats:
                    cat.heal()
            elif check_button_click(buy_food_button_rect.x, buy_food_button_rect.y, buy_food_button_rect.width, buy_food_button_rect.height, mouse_pos):
                if currency >= 10:
                    currency -= 10
                    food += 10
            elif check_button_click(buy_water_button_rect.x, buy_water_button_rect.y, buy_water_button_rect.width, buy_water_button_rect.height, mouse_pos):
                if currency >= 10:
                    currency -= 10
                    water += 10
            elif check_button_click(gather_resources_button_rect.x, gather_resources_button_rect.y, gather_resources_button_rect.width, gather_resources_button_rect.height, mouse_pos):
                food += random.randint(5, 15)
                water += random.randint(5, 15)
            elif check_button_click(earn_money_button_rect.x, earn_money_button_rect.y, earn_money_button_rect.width, earn_money_button_rect.height, mouse_pos):
                currency += random.randint(10, 20)

    # Update the game
    all_sprites.update()

    # Handle random events
    event_timer += clock.get_time()
    if event_timer >= event_interval:
        random_event = generate_random_event()
        event_message = handle_random_event(random_event, create_new_cat)
        event_timer = 0

        # Randomly change weather
        weather = random.choice(["Sunny", "Rainy", "Windy", "Snowy"])

    # Update time of day
    time_of_day = (time_of_day + 1) % day_length

    # Clear the screen
    screen.fill(WHITE)

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw status bars for each cat
    for cat in cats:
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 10, cat.health, 100, RED, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 20, cat.hunger, 100, BLUE, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 30, cat.thirst, 100, GREEN, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 40, cat.cleanliness, 100, BLACK, width=70)

    # Draw UI buttons
    draw_button(screen, feed_button_rect.x, feed_button_rect.y, feed_button_rect.width, feed_button_rect.height, "Feed Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, water_button_rect.x, water_button_rect.y, water_button_rect.width, water_button_rect.height, "Water Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, shelter_button_rect.x, shelter_button_rect.y, shelter_button_rect.width, shelter_button_rect.height, "Build Shelter", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, clean_button_rect.x, clean_button_rect.y, clean_button_rect.width, clean_button_rect.height, "Clean Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, heal_button_rect.x, heal_button_rect.y, heal_button_rect.width, heal_button_rect.height, "Heal Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, buy_food_button_rect.x, buy_food_button_rect.y, buy_food_button_rect.width, buy_food_button_rect.height, "Buy Food", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, buy_water_button_rect.x, buy_water_button_rect.y, buy_water_button_rect.width, buy_water_button_rect.height, "Buy Water", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, gather_resources_button_rect.x, gather_resources_button_rect.y, gather_resources_button_rect.width, gather_resources_button_rect.height, "Gather Resources", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, earn_money_button_rect.x, earn_money_button_rect.y, earn_money_button_rect.width, earn_money_button_rect.height, "Earn Money", BUTTON_COLOR, BUTTON_TEXT_COLOR)

    # Display random event message
    if event_message:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(event_message, True, BLACK)
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 60))

    # Display food, water, weather, time of day, and currency
    font = pygame.font.Font(None, 36)
    food_text = font.render(f"Food: {food}", True, BLACK)
    water_text = font.render(f"Water: {water}", True, BLACK)
    weather_text = font.render(f"Weather: {weather}", True, BLACK)
    time_of_day_text = font.render(f"Time of Day: {'Day' if time_of_day < 1200 else 'Night'}", True, BLACK)
    currency_text = font.render(f"Money: ${currency}", True, BLACK)
    screen.blit(food_text, (20, 180))
    screen.blit(water_text, (240, 180))
    screen.blit(weather_text, (460, 180))
    screen.blit(time_of_day_text, (680, 180))
    screen.blit(currency_text, (900, 180))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
