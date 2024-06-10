import pygame
import random
from status_bar import draw_status_bar
from ui import draw_button, check_button_click
from random_events import generate_random_event, handle_random_event
from sprite_loader import load_cat_sprites, load_shelter_sprites

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
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (173, 216, 230)
BUTTON_COLOR = (100, 100, 200)
BUTTON_TEXT_COLOR = WHITE

# Load and resize cat images
cat_size = (50, 50)  # Desired size for cat sprites
cat_images = load_cat_sprites('assets/cats', cat_size)

# Load and resize shelter images
shelter_sizes = [(100, 100), (150, 150), (200, 200)]  # Add more sizes as needed
shelter_images = load_shelter_sprites('assets/shelters', shelter_sizes)

# Resource management
food = 100
water = 100
currency = 100  # New currency system

# Weather system
current_weather = "Sunny"
weather_effects = {
    "Sunny": {"hunger": 0.01, "thirst": 0.01},
    "Cloudy": {"hunger": 0.01, "thirst": 0.01},
    "Rainy": {"hunger": 0.02, "thirst": 0.01},
    "Heat Wave": {"hunger": 0.05, "thirst": 0.05},
    "Snow Storm": {"hunger": 0.04, "thirst": 0.03}
}
weather_probabilities = {
    "spring": {"Sunny": 0.5, "Cloudy": 0.3, "Rainy": 0.2},
    "summer": {"Sunny": 0.6, "Cloudy": 0.2, "Rainy": 0.1, "Heat Wave": 0.1},
    "autumn": {"Sunny": 0.5, "Cloudy": 0.3, "Rainy": 0.2},
    "winter": {"Sunny": 0.3, "Cloudy": 0.3, "Rainy": 0.1, "Snow Storm": 0.3}
}

# Time and season system
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
seasons = {"spring": ["March", "April", "May"], "summer": ["June", "July", "August"], "autumn": ["September", "October", "November"], "winter": ["December", "January", "February"]}
current_month_index = 0
current_day = 1
current_year = 2024
day_length = 2400  # Total number of ticks in a day
time_of_day = 0  # 0 to 2399, where 0-1199 is day and 1200-2399 is night

# Weather particles
snowflakes = []
raindrops = []

def create_snowflakes(num):
    for _ in range(num):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(-SCREEN_HEIGHT, 0)
        snowflakes.append([x, y])

def create_raindrops(num):
    for _ in range(num):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(-SCREEN_HEIGHT, 0)
        raindrops.append([x, y])

def update_snowflakes():
    for flake in snowflakes:
        flake[1] += 1
        if flake[1] > SCREEN_HEIGHT:
            flake[1] = random.randint(-SCREEN_HEIGHT, 0)
            flake[0] = random.randint(0, SCREEN_WIDTH)

def update_raindrops():
    for drop in raindrops:
        drop[1] += 5
        if drop[1] > SCREEN_HEIGHT:
            drop[1] = random.randint(-SCREEN_HEIGHT, 0)
            drop[0] = random.randint(0, SCREEN_WIDTH)

# Define Cat sprite with personalities
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
        self.speed = random.uniform(1, 3)  # Speed varies between 1 and 3
        self.direction = random.choice(["left", "right", "up", "down"])
        self.move_counter = 0
        self.rest_counter = 0
        self.personality = random.choice(["active", "lazy", "curious", "timid"])

    def update(self):
        global current_weather
        global time_of_day
        # Behavior affected by weather and time of day
        hunger_rate = weather_effects[current_weather]["hunger"]
        thirst_rate = weather_effects[current_weather]["thirst"]

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
        else:
            self.wander()

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
        if self.health > 100:
            self.health = 100

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
            self.rect.x += dx * self.speed  # Move speed
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
                if self.rect.x < 0: self.rect.x = SCREEN_WIDTH
            elif self.direction == "right":
                self.rect.x += self.speed
                if self.rect.x > SCREEN_WIDTH: self.rect.x = 0
            elif self.direction == "up":
                self.rect.y -= self.speed
                if self.rect.y < 0: self.rect.y = SCREEN_HEIGHT
            elif self.direction == "down":
                self.rect.y += self.speed
                if self.rect.y > SCREEN_HEIGHT: self.rect.y = 0

# Define Shelter sprite
class Shelter(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = random.choice(shelter_images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Helper function to create a new cat
def create_new_cat():
    if len(cats) < 15:
        new_cat = Cat()
        all_sprites.add(new_cat)
        cats.add(new_cat)

# Function to convert time_of_day to HH:MM format
def format_time_of_day(ticks):
    hours = (ticks // 100) % 24
    minutes = (ticks % 100) * 60 // 100
    return f"{hours:02}:{minutes:02}"

# Function to get current season
def get_current_season():
    month = months[current_month_index]
    for season, season_months in seasons.items():
        if month in season_months:
            return season
    return "spring"  # Default to spring

# Function to determine the next weather event based on the current season
def determine_next_weather():
    season = get_current_season()
    probabilities = weather_probabilities[season]
    weather_event = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]
    return weather_event

# Initialize the game window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Cat Colony Simulator")

# Sprite groups
all_sprites = pygame.sprite.Group()
cats = pygame.sprite.Group()
shelters = pygame.sprite.Group()

# Create initial cats
initial_cats = random.randint(4, 6)
for _ in range(initial_cats):
    cat = Cat()
    all_sprites.add(cat)
    cats.add(cat)

# Initialize snowflakes and raindrops
create_snowflakes(100)
create_raindrops(100)

# Main game loop
running = True
paused = False
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
pause_button_rect = pygame.Rect(900, 100, 200, 60)  # Button for pausing the game

# Random event timer
event_timer = 0
event_interval = 5000  # 5 seconds
event_message = ""

# Weather update timer
weather_timer = 0
weather_interval = 60000  # 60 seconds

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
            elif check_button_click(pause_button_rect.x, pause_button_rect.y, pause_button_rect.width, pause_button_rect.height, mouse_pos):
                paused = not paused

    if not paused:
        # Update the game
        all_sprites.update()

        # Handle random events
        event_timer += clock.get_time()
        if event_timer >= event_interval:
            random_event = generate_random_event(len(cats))
            event_message = handle_random_event(random_event, create_new_cat)
            event_timer = 0

        # Update weather
        weather_timer += clock.get_time()
        if weather_timer >= weather_interval:
            current_weather = determine_next_weather()
            weather_timer = 0

        # Update time of day
        time_of_day = (time_of_day + 1) % day_length

        # Update day, month, and year
        if time_of_day == 0:
            current_day += 1
            if current_day > 30:  # Simplified month length
                current_day = 1
                current_month_index = (current_month_index + 1) % 12
                if current_month_index == 0:
                    current_year += 1

        # Update snowflakes and raindrops
        if current_weather == "Snow Storm":
            update_snowflakes()
        elif current_weather == "Rainy":
            update_raindrops()

    # Clear the screen
    screen.fill(WHITE)

    # Draw weather effects
    if current_weather == "Sunny":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(YELLOW)
        screen.blit(overlay, (0, 0))
    elif current_weather == "Cloudy":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(GREY)
        screen.blit(overlay, (0, 0))
    elif current_weather == "Rainy":
        for drop in raindrops:
            pygame.draw.line(screen, LIGHT_BLUE, (drop[0], drop[1]), (drop[0], drop[1] + 5), 1)
    elif current_weather == "Snow Storm":
        for flake in snowflakes:
            pygame.draw.circle(screen, WHITE, (flake[0], flake[1]), 3)
    elif current_weather == "Heat Wave":
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(RED)
        screen.blit(overlay, (0, 0))

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
    draw_button(screen, pause_button_rect.x, pause_button_rect.y, pause_button_rect.width, pause_button_rect.height, "Pause" if not paused else "Resume", BUTTON_COLOR, BUTTON_TEXT_COLOR)

    # Display random event message
    if event_message:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(event_message, True, BLACK)
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 60))

    # Display food, water, weather, time of day, and currency
    font = pygame.font.Font(None, 36)
    food_text = font.render(f"Food: {food}", True, BLACK)
    water_text = font.render(f"Water: {water}", True, BLACK)
    weather_text = font.render(f"Weather: {current_weather}", True, BLACK)
    time_of_day_text = font.render(f"Time: {format_time_of_day(time_of_day)}", True, BLACK)
    date_text = font.render(f"Date: {months[current_month_index]} {current_day}, {current_year}", True, BLACK)
    currency_text = font.render(f"Money: ${currency}", True, BLACK)
    screen.blit(food_text, (20, 180))
    screen.blit(water_text, (240, 180))
    screen.blit(weather_text, (460, 180))
    screen.blit(time_of_day_text, (680, 180))
    screen.blit(date_text, (900, 180))
    screen.blit(currency_text, (1120, 180))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
