import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class WeatherManager:
    def __init__(self):
        self.time_of_day = 600  # Start at 6:00 AM
        self.current_weather = "Sunny"
        self.seasons = ["Spring", "Summer", "Autumn", "Winter"]
        self.season = "Spring"
        self.date = {
            'day': 1,
            'month': 'January',
            'year': 2024
        }
        self.currency = 100
        self.weather_effects = []
        self.weather_timer = 0

    def update_weather(self, delta_time):
        self.weather_timer += delta_time
        if self.weather_timer > 10000:  # Change weather every 10 seconds for demonstration
            self.current_weather = random.choice(["Sunny", "Cloudy", "Rain", "Snow"])
            self.weather_timer = 0
            self.update_weather_effects()

    def update_time(self, speed):
        self.time_of_day += speed
        if self.time_of_day >= 2400:
            self.time_of_day = 0
            self.date['day'] += 1
            if self.date['day'] > 30:
                self.date['day'] = 1
                self.update_season()
                self.update_month()

    def update_season(self):
        current_season_index = self.seasons.index(self.season)
        next_season_index = (current_season_index + 1) % len(self.seasons)
        self.season = self.seasons[next_season_index]

    def update_month(self):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        current_month_index = months.index(self.date['month'])
        next_month_index = (current_month_index + 1) % len(months)
        self.date['month'] = months[next_month_index]
        if next_month_index == 0:
            self.date['year'] += 1

    def update_weather_effects(self):
        self.weather_effects = []
        if self.current_weather == "Rain":
            for _ in range(100):
                self.weather_effects.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(0, SCREEN_HEIGHT),
                    'speed': random.uniform(2, 5)
                })
        elif self.current_weather == "Snow":
            for _ in range(100):
                self.weather_effects.append({
                    'x': random.randint(0, SCREEN_WIDTH),
                    'y': random.randint(0, SCREEN_HEIGHT),
                    'speed': random.uniform(1, 3)
                })

    def draw_weather_effects(self, screen):
        if self.current_weather == "Rain":
            for drop in self.weather_effects:
                drop['y'] += drop['speed']
                if drop['y'] > SCREEN_HEIGHT:
                    drop['y'] = 0
                    drop['x'] = random.randint(0, SCREEN_WIDTH)
                pygame.draw.line(screen, (0, 0, 255), (drop['x'], drop['y']), (drop['x'], drop['y'] + 5), 2)
        elif self.current_weather == "Snow":
            for flake in self.weather_effects:
                flake['y'] += flake['speed']
                if flake['y'] > SCREEN_HEIGHT:
                    flake['y'] = 0
                    flake['x'] = random.randint(0, SCREEN_WIDTH)
                pygame.draw.circle(screen, (255, 255, 255), (flake['x'], flake['y']), 2)
