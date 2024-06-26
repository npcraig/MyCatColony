import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BUTTON_COLOR, BUTTON_TEXT_COLOR, RED, BLUE, GREEN, BLACK, set_resolution, get_available_resolutions
from weather import WeatherManager
from sprites.cat import Cat
from sprites.shelter import Shelter
from sprites.player import Player
from sprites.food import Food
from sprites.water import Water
from ui.status_bar import draw_status_bar
from ui.buttons import draw_button, check_button_click
from random_events import generate_random_event, handle_random_event
from utils.sprite_loader import load_cat_sprites, load_shelter_sprites
from inventory import Inventory
from game_save_load import save_game, load_game
from math import sin, cos, radians
from traits import inherit_traits
from achievements import Achievements
from fundraising import Fundraising, FundraisingEvent
from cat_cafe import CatCafe
from educational_tips import EducationalTips

# Initialize Pygame
pygame.init()

# Initialize the game window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Cat Colony Simulator")

# Load and resize cat images
cat_images = load_cat_sprites('assets/cats', (50, 50))
# Load and resize player image
player_image = pygame.image.load('assets/player.png')
player_image = pygame.transform.scale(player_image, (50, 50))

# Load and resize food, water, and shelter images
food_image = pygame.image.load('assets/food.png')
food_image = pygame.transform.scale(food_image, (30, 30))
water_image = pygame.image.load('assets/water.png')
water_image = pygame.transform.scale(water_image, (30, 30))
shelter_images = load_shelter_sprites('assets/shelters', [(100, 100), (150, 150), (200, 200)])

# Initialize weather manager
weather_manager = WeatherManager()

# Initialize inventory
inventory = Inventory()

# Initialize achievements
achievements = Achievements()

# Initialize fundraising
fundraising = Fundraising()

# Initialize cat café
cat_cafe = CatCafe()

# Initialize educational tips
educational_tips = EducationalTips()

# Sprite groups
all_sprites = pygame.sprite.Group()
cats = pygame.sprite.Group()
foods = pygame.sprite.Group()
waters = pygame.sprite.Group()
shelters = pygame.sprite.Group()

# Create player
player = Player(player_image)
all_sprites.add(player)

# Create initial cats
for _ in range(random.randint(4, 6)):
    cat = Cat(cat_images, shelters)
    all_sprites.add(cat)
    cats.add(cat)

# Helper function to create a new cat
def create_new_cat():
    if len(cats) < 15:
        new_cat = Cat(cat_images, shelters)
        all_sprites.add(new_cat)
        cats.add(new_cat)
        achievements.unlock("First Cat")
        if len(cats) == 10:
            achievements.unlock("Ten Cats")

# Breeding function
def breed_cats(cat1, cat2):
    if len(cats) < 15:
        new_traits = inherit_traits(cat1.traits, cat2.traits)
        new_cat = Cat(cat_images, shelters, traits=new_traits)
        all_sprites.add(new_cat)
        cats.add(new_cat)

# Adoption function
def put_up_for_adoption(cat):
    cats.remove(cat)
    all_sprites.remove(cat)

# Define available fundraising events
fundraising_events = [
    FundraisingEvent("Bake Sale", 60, 2),  # duration 60 seconds, $2 per second
    FundraisingEvent("Charity Run", 120, 1.5),  # duration 120 seconds, $1.5 per second
    FundraisingEvent("Community Auction", 180, 3),  # duration 180 seconds, $3 per second
]

# Main game loop
running = True
paused = False
clock = pygame.time.Clock()
selected_cat = None  # Variable to store the selected cat
fundraising_menu_open = False  # Variable to track if the fundraising menu is open
settings_menu_open = False  # Variable to track if the settings menu is open

# Time speed settings
time_speeds = [0.5, 1, 2, 3]
current_time_speed_index = 1  # Start at 1x speed
time_speed = time_speeds[current_time_speed_index]

# UI positions
button_width = 200
button_height = 60
button_spacing = 20
top_margin = 20

button_rects = [
    pygame.Rect(20, top_margin, button_width, button_height),
    pygame.Rect(240, top_margin, button_width, button_height),
    pygame.Rect(460, top_margin, button_width, button_height),
    pygame.Rect(680, top_margin, button_width, button_height),
    pygame.Rect(900, top_margin, button_width, button_height),
    pygame.Rect(20, top_margin + button_height + button_spacing, button_width, button_height),
    pygame.Rect(240, top_margin + button_height + button_spacing, button_width, button_height),
    pygame.Rect(460, top_margin + button_height + button_spacing, button_width, button_height),
    pygame.Rect(680, top_margin + button_height + button_spacing, button_width, button_height),
    pygame.Rect(900, top_margin + button_height + button_spacing, button_width, button_height),
    pygame.Rect(1120, top_margin, button_width, button_height),  # Button for changing time speed
    pygame.Rect(1340, top_margin, button_width, button_height),  # Button for saving game
    pygame.Rect(1560, top_margin, button_width, button_height),   # Button for loading game
    pygame.Rect(1780, top_margin, button_width, button_height),   # Button for breeding cats
    pygame.Rect(1780, top_margin + button_height + button_spacing, button_width, button_height),  # Button for putting cats up for adoption
    pygame.Rect(1780, top_margin + 2 * (button_height + button_spacing), button_width, button_height),  # Button for organizing fundraising event
    pygame.Rect(1780, top_margin + 3 * (button_height + button_spacing), button_width, button_height)  # Button for settings
]

fundraising_event_button_rects = [
    pygame.Rect(20, SCREEN_HEIGHT // 2, button_width, button_height),
    pygame.Rect(240, SCREEN_HEIGHT // 2, button_width, button_height),
    pygame.Rect(460, SCREEN_HEIGHT // 2, button_width, button_height),
]

settings_button_rects = [
    pygame.Rect(20, SCREEN_HEIGHT // 2 + i * (button_height + button_spacing), button_width, button_height)
    for i in range(10)  # Adjust this range to fit the number of resolutions you want to display
]

# Assign buttons to variables for easy access
(feed_button_rect, water_button_rect, shelter_button_rect, clean_button_rect, heal_button_rect, 
 buy_food_button_rect, buy_water_button_rect, gather_resources_button_rect, 
 earn_money_button_rect, pause_button_rect, time_speed_button_rect, save_button_rect, load_button_rect, breed_button_rect, adopt_button_rect, fundraising_button_rect, settings_button_rect) = button_rects

# Random event timer
event_timer = 0
event_interval = 5000  # 5 seconds
event_message = ""

def draw_analog_clock(screen, x, y, radius, time_of_day):
    pygame.draw.circle(screen, BLACK, (x, y), radius)
    pygame.draw.circle(screen, WHITE, (x, y), radius - 5)

    hours = (time_of_day // 100) % 24
    minutes = (time_of_day % 100) * 60 // 100

    # Calculate the angles for the hour and minute hands
    hour_angle = radians((hours % 12) * 30 - 90)
    minute_angle = radians(minutes * 6 - 90)

    # Draw the hour hand
    hour_hand_length = radius * 0.5
    hour_x = x + int(hour_hand_length * cos(hour_angle))
    hour_y = y + int(hour_hand_length * sin(hour_angle))
    pygame.draw.line(screen, BLACK, (x, y), (hour_x, hour_y), 4)

    # Draw the minute hand
    minute_hand_length = radius * 0.8
    minute_x = x + int(minute_hand_length * cos(minute_angle))
    minute_y = y + int(minute_hand_length * sin(minute_angle))
    pygame.draw.line(screen, BLACK, (x, y), (minute_x, minute_y), 2)

def open_settings_menu():
    global screen, SCREEN_WIDTH, SCREEN_HEIGHT, settings_menu_open
    resolutions = get_available_resolutions()
    selected_resolution_index = 0

    settings_menu_running = True
    while settings_menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings_menu_running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, rect in enumerate(settings_button_rects):
                    if check_button_click(rect, mouse_pos):
                        selected_resolution_index = i
                        set_resolution(resolutions[i][0], resolutions[i][1])
                        screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
                if check_button_click(return_button_rect, mouse_pos):
                    settings_menu_running = False

        # Clear the screen
        screen.fill(WHITE)

        # Draw settings menu buttons
        settings_labels = [f"{res[0]}x{res[1]}" for res in resolutions]
        for rect, label in zip(settings_button_rects, settings_labels):
            draw_button(screen, rect, label, BUTTON_COLOR, BUTTON_TEXT_COLOR)

        # Draw return button
        draw_button(screen, return_button_rect, "Return", BUTTON_COLOR, BUTTON_TEXT_COLOR)

        pygame.display.flip()

    settings_menu_open = False
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

return_button_rect = pygame.Rect(20, SCREEN_HEIGHT // 2 + 11 * (button_height + button_spacing), button_width, button_height)

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if fundraising_menu_open:
                # Check for clicks on fundraising event buttons
                for i, rect in enumerate(fundraising_event_button_rects):
                    if check_button_click(rect, mouse_pos):
                        fundraising.start_event(fundraising_events[i])
                        fundraising_menu_open = False
                        break
            elif settings_menu_open:
                # Check for clicks on settings buttons
                open_settings_menu()
                settings_menu_open = False
            else:
                if check_button_click(feed_button_rect, mouse_pos):
                    if inventory.food > 0:
                        inventory.food -= 1
                        new_food = Food(player.rect.x, player.rect.y, food_image)
                        all_sprites.add(new_food)
                        foods.add(new_food)
                elif check_button_click(water_button_rect, mouse_pos):
                    if inventory.water > 0:
                        inventory.water -= 1
                        new_water = Water(player.rect.x, player.rect.y, water_image)
                        all_sprites.add(new_water)
                        waters.add(new_water)
                elif check_button_click(shelter_button_rect, mouse_pos):
                    x, y = player.rect.x, player.rect.y
                    shelter = Shelter(x, y, shelter_images)
                    all_sprites.add(shelter)
                    shelters.add(shelter)
                    achievements.unlock("First Shelter")
                elif check_button_click(clean_button_rect, mouse_pos):
                    for cat in cats:
                        cat.clean()
                elif check_button_click(heal_button_rect, mouse_pos):
                    for cat in cats:
                        cat.heal()
                elif check_button_click(buy_food_button_rect, mouse_pos):
                    if inventory.spend_money(10):  # Assume each food costs $10
                        inventory.add_food(1)
                        if inventory.money >= 100:
                            achievements.unlock("Hundred Dollars")
                elif check_button_click(buy_water_button_rect, mouse_pos):
                    if inventory.spend_money(5):  # Assume each water costs $5
                        inventory.add_water(1)
                elif check_button_click(gather_resources_button_rect, mouse_pos):
                    # Implement gathering resources logic
                    pass
                elif check_button_click(earn_money_button_rect, mouse_pos):
                    inventory.earn_money(20)  # Example of earning money
                elif check_button_click(pause_button_rect, mouse_pos):
                    paused = not paused
                elif check_button_click(time_speed_button_rect, mouse_pos):
                    current_time_speed_index = (current_time_speed_index + 1) % len(time_speeds)
                    time_speed = time_speeds[current_time_speed_index]
                elif check_button_click(save_button_rect, mouse_pos):
                    save_game('savegame.json', player, cats, shelters, foods, waters, inventory, weather_manager)
                elif check_button_click(load_button_rect, mouse_pos):
                    load_game('savegame.json', player, cats, shelters, foods, waters, inventory, weather_manager, cat_images, shelter_images, food_image, water_image)
                elif check_button_click(breed_button_rect, mouse_pos):
                    # Select two random cats to breed
                    if len(cats) >= 2:
                        cat1, cat2 = random.sample(cats.sprites(), 2)
                        breed_cats(cat1, cat2)
                elif check_button_click(adopt_button_rect, mouse_pos) and selected_cat:
                    put_up_for_adoption(selected_cat)
                elif check_button_click(fundraising_button_rect, mouse_pos):
                    fundraising_menu_open = True
                elif check_button_click(settings_button_rect, mouse_pos):
                    settings_menu_open = True
                else:
                    # Check for clicks on cats
                    for cat in cats:
                        if cat.rect.collidepoint(mouse_pos):
                            selected_cat = cat
                            break

    if not paused:
        # Update the game
        player.update(keys)
        cats.update(foods, waters, cats)
        fundraising.update_events(clock.get_time() * 0.001 * time_speed)  # Convert milliseconds to seconds

        # Handle random events
        event_timer += clock.get_time()
        if event_timer >= event_interval:
            random_event = generate_random_event(len(cats))
            event_message = handle_random_event(random_event, create_new_cat)
            event_timer = 0

        # Update weather
        weather_manager.update_weather(clock.get_time() * time_speed)

        # Update time of day
        weather_manager.update_time(time_speed)

    # Clear the screen
    screen.fill(WHITE)

    # Draw weather effects
    weather_manager.draw_weather_effects(screen)

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw status bars for each cat
    for cat in cats:
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 40, cat.health, 100, RED, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 30, cat.hunger, 100, BLUE, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 20, cat.thirst, 100, GREEN, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 10, cat.cleanliness, 100, BLACK, width=70)

    # Draw UI buttons
    button_labels = ["Feed Cats", "Water Cats", "Build Shelter", "Clean Cats", "Heal Cats",
                     "Buy Food", "Buy Water", "Gather Resources", "Earn Money", 
                     "Pause" if not paused else "Resume", f"Speed: {time_speed}x", "Save Game", "Load Game", "Breed Cats", "Adopt Cat", "Fundraising", "Settings"]

    for rect, label in zip(button_rects, button_labels):
        draw_button(screen, rect, label, BUTTON_COLOR, BUTTON_TEXT_COLOR)

    if fundraising_menu_open:
        # Draw fundraising menu
        menu_labels = ["Bake Sale", "Charity Run", "Community Auction"]
        for rect, label in zip(fundraising_event_button_rects, menu_labels):
            draw_button(screen, rect, label, BUTTON_COLOR, BUTTON_TEXT_COLOR)

    # Display random event message
    if event_message:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(event_message, True, BLACK)
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 60))

    # Display inventory status
    font = pygame.font.Font(None, 36)
    inventory_text = font.render(inventory.get_status(), True, BLACK)
    screen.blit(inventory_text, (20, 180))

    # Display fundraising funds
    funds_text = font.render(f"Funds: ${fundraising.get_funds():.2f}", True, BLACK)
    screen.blit(funds_text, (20, 220))

    # Draw analog clock
    draw_analog_clock(screen, 1120 + button_width // 2, 180 + button_height // 2, 40, weather_manager.time_of_day)

    # Draw detailed status panel for the selected cat
    if selected_cat:
        panel_width = 300
        panel_height = 200
        panel_x = SCREEN_WIDTH - panel_width - 20
        panel_y = SCREEN_HEIGHT - panel_height - 20
        pygame.draw.rect(screen, BLACK, (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(screen, WHITE, (panel_x + 5, panel_y + 5, panel_width - 10, panel_height - 10))

        status_text = f"Name: {selected_cat.name}\nBreed: {selected_cat.breed}\nFur Color: {selected_cat.fur_color}\nEye Color: {selected_cat.eye_color}\nPersonality: {selected_cat.personality}\n\nHealth: {selected_cat.health}\nHunger: {selected_cat.hunger}\nThirst: {selected_cat.thirst}\nCleanliness: {selected_cat.cleanliness}"
        font = pygame.font.Font(None, 28)
        y_offset = panel_y + 10
        for line in status_text.split('\n'):
            text_surface = font.render(line, True, BLACK)
            screen.blit(text_surface, (panel_x + 10, y_offset))
            y_offset += 30

    # Display current educational tip
    font = pygame.font.Font(None, 24)
    tip_text = font.render(f"Tip: {educational_tips.get_current_tip()}", True, BLACK)
    screen.blit(tip_text, (20, SCREEN_HEIGHT - 30))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
