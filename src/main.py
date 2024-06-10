import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BUTTON_COLOR, BUTTON_TEXT_COLOR, RED, BLUE, GREEN, BLACK
from weather import WeatherManager
from sprites.cat import Cat
from sprites.shelter import Shelter
from ui.status_bar import draw_status_bar
from ui.buttons import draw_button, check_button_click
from random_events import generate_random_event, handle_random_event
from utilities.sprite_loader import load_cat_sprites, load_shelter_sprites

# Initialize Pygame
pygame.init()

# Initialize the game window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Cat Colony Simulator")

# Load and resize cat images
cat_images = load_cat_sprites('assets/cats', (50, 50))

# Load and resize shelter images
shelter_images = load_shelter_sprites('assets/shelters', [(100, 100), (150, 150), (200, 200)])

# Initialize weather manager
weather_manager = WeatherManager()

# Sprite groups
all_sprites = pygame.sprite.Group()
cats = pygame.sprite.Group()
shelters = pygame.sprite.Group()

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
earn_money_button_rect = pygame.Rect(680, 100, 200, 60)
pause_button_rect = pygame.Rect(900, 100, 200, 60)

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
            if check_button_click(feed_button_rect, mouse_pos):
                for cat in cats:
                    cat.feed()
            elif check_button_click(water_button_rect, mouse_pos):
                for cat in cats:
                    cat.give_water()
            elif check_button_click(shelter_button_rect, mouse_pos):
                x, y = random.randint(0, SCREEN_WIDTH - 100), random.randint(0, SCREEN_HEIGHT - 100)
                shelter = Shelter(x, y, shelter_images)
                all_sprites.add(shelter)
                shelters.add(shelter)
            elif check_button_click(clean_button_rect, mouse_pos):
                for cat in cats:
                    cat.clean()
            elif check_button_click(heal_button_rect, mouse_pos):
                for cat in cats:
                    cat.heal()
            elif check_button_click(buy_food_button_rect, mouse_pos):
                # Implement buying food logic
                pass
            elif check_button_click(buy_water_button_rect, mouse_pos):
                # Implement buying water logic
                pass
            elif check_button_click(gather_resources_button_rect, mouse_pos):
                # Implement gathering resources logic
                pass
            elif check_button_click(earn_money_button_rect, mouse_pos):
                # Implement earning money logic
                pass
            elif check_button_click(pause_button_rect, mouse_pos):
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
        weather_manager.update_weather(clock.get_time())

        # Update time of day
        weather_manager.update_time()

    # Clear the screen
    screen.fill(WHITE)

    # Draw weather effects
    weather_manager.draw_weather_effects(screen)

    # Draw all sprites
    all_sprites.draw(screen)

    # Draw status bars for each cat
    for cat in cats:
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 10, cat.health, 100, RED, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 20, cat.hunger, 100, BLUE, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 30, cat.thirst, 100, GREEN, width=70)
        draw_status_bar(screen, cat.rect.x, cat.rect.y - 40, cat.cleanliness, 100, BLACK, width=70)

    # Draw UI buttons
    draw_button(screen, feed_button_rect, "Feed Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, water_button_rect, "Water Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, shelter_button_rect, "Build Shelter", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, clean_button_rect, "Clean Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, heal_button_rect, "Heal Cats", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, buy_food_button_rect, "Buy Food", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, buy_water_button_rect, "Buy Water", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, gather_resources_button_rect, "Gather Resources", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, earn_money_button_rect, "Earn Money", BUTTON_COLOR, BUTTON_TEXT_COLOR)
    draw_button(screen, pause_button_rect, "Pause" if not paused else "Resume", BUTTON_COLOR, BUTTON_TEXT_COLOR)

    # Display random event message
    if event_message:
        font = pygame.font.Font(None, 36)
        text_surface = font.render(event_message, True, BLACK)
        screen.blit(text_surface, (20, SCREEN_HEIGHT - 60))

    # Display food, water, weather, time of day, and currency
    font = pygame.font.Font(None, 36)
    food_text = font.render(f"Food: {weather_manager.food}", True, BLACK)
    water_text = font.render(f"Water: {weather_manager.water}", True, BLACK)
    weather_text = font.render(f"Weather: {weather_manager.current_weather}", True, BLACK)
    time_of_day_text = font.render(f"Time: {weather_manager.format_time_of_day()}", True, BLACK)
    date_text = font.render(f"Date: {weather_manager.current_date()}", True, BLACK)
    currency_text = font.render(f"Money: ${weather_manager.currency}", True, BLACK)
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
