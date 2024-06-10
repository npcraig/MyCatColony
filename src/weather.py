import pygame
import random

class WeatherManager:
    def __init__(self):
        self.weather = "Sunny"
        self.time_of_day = 600  # Represents 6:00 AM
        self.season = "Spring"
        self.seasons = ["Spring", "Summer", "Fall", "Winter"]
        self.weather_effects = []

    def update_weather(self, delta_time):
        if self.weather == "Rainy":
            self.weather_effects.append(RainEffect())

    def update_time(self, time_speed):
        self.time_of_day += time_speed
        if self.time_of_day >= 2400:
            self.time_of_day -= 2400
            self.advance_season()

    def advance_season(self):
        current_index = self.seasons.index(self.season)
        next_index = (current_index + 1) % len(self.seasons)
        self.season = self.seasons[next_index]

    def draw_weather_effects(self, screen):
        for effect in self.weather_effects:
            effect.draw(screen)

class RainEffect:
    def __init__(self):
        self.drops = [pygame.Rect(random.randint(0, 1920), random.randint(0, 1080), 2, 10) for _ in range(100)]

    def draw(self, screen):
        for drop in self.drops:
            drop.y += 5
            if drop.y > 1080:
                drop.y = random.randint(-10, -1)
            pygame.draw.rect(screen, (0, 0, 255), drop)
