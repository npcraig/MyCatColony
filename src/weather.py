import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW, GREY, LIGHT_BLUE, WHITE, RED

class WeatherManager:
    def __init__(self):
        self.current_weather = "Sunny"
        self.weather_effects = {
            "Sunny": {"hunger": 0.01, "thirst": 0.01},
            "Cloudy": {"hunger": 0.01, "thirst": 0.01},
            "Rainy": {"hunger": 0.02, "thirst": 0.01},
            "Heat Wave": {"hunger": 0.05, "thirst": 0.05},
            "Snow Storm": {"hunger": 0.04, "thirst": 0.03}
        }
        self.weather_probabilities = {
            "spring": {"Sunny": 0.5, "Cloudy": 0.3, "Rainy": 0.2},
            "summer": {"Sunny": 0.6, "Cloudy": 0.2, "Rainy": 0.1, "Heat Wave": 0.1},
            "autumn": {"Sunny": 0.5, "Cloudy": 0.3, "Rainy": 0.2},
            "winter": {"Sunny": 0.3, "Cloudy": 0.3, "Rainy": 0.1, "Snow Storm": 0.3}
        }
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        self.seasons = {"spring": ["March", "April", "May"], "summer": ["June", "July", "August"], "autumn": ["September", "October", "November"], "winter": ["December", "January", "February"]}
        self.current_month_index = 0
        self.current_day = 1
        self.current_year = 2024
        self.day_length = 2400  # Total number of ticks in a day
        self.time_of_day = 0  # 0 to 2399, where 0-1199 is day and 1200-2399 is night
        self.snowflakes = []
        self.raindrops = []
        self.food = 100
        self.water = 100
        self.currency = 100
        self.create_snowflakes(100)
        self.create_raindrops(100)

    def create_snowflakes(self, num):
        for _ in range(num):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-SCREEN_HEIGHT, 0)
            self.snowflakes.append([x, y])

    def create_raindrops(self, num):
        for _ in range(num):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(-SCREEN_HEIGHT, 0)
            self.raindrops.append([x, y])

    def update_snowflakes(self):
        for flake in self.snowflakes:
            flake[1] += 1
            if flake[1] > SCREEN_HEIGHT:
                flake[1] = random.randint(-SCREEN_HEIGHT, 0)
                flake[0] = random.randint(0, SCREEN_WIDTH)

    def update_raindrops(self):
        for drop in self.raindrops:
            drop[1] += 5
            if drop[1] > SCREEN_HEIGHT:
                drop[1] = random.randint(-SCREEN_HEIGHT, 0)
                drop[0] = random.randint(0, SCREEN_WIDTH)

    def update_weather(self, time_elapsed):
        self.time_of_day += time_elapsed
        if self.time_of_day >= self.day_length:
            self.time_of_day = 0
            self.current_day += 1
            if self.current_day > 30:  # Simplified month length
                self.current_day = 1
                self.current_month_index = (self.current_month_index + 1) % 12
                if self.current_month_index == 0:
                    self.current_year += 1
            self.current_weather = self.determine_next_weather()

        if self.current_weather == "Snow Storm":
            self.update_snowflakes()
        elif self.current_weather == "Rainy":
            self.update_raindrops()

    def update_time(self):
        self.time_of_day = (self.time_of_day + 1) % self.day_length

    def draw_weather_effects(self, screen):
        if self.current_weather == "Sunny":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(YELLOW)
            screen.blit(overlay, (0, 0))
        elif self.current_weather == "Cloudy":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(GREY)
            screen.blit(overlay, (0, 0))
        elif self.current_weather == "Rainy":
            for drop in self.raindrops:
                pygame.draw.line(screen, LIGHT_BLUE, (drop[0], drop[1]), (drop[0], drop[1] + 5), 1)
        elif self.current_weather == "Snow Storm":
            for flake in self.snowflakes:
                pygame.draw.circle(screen, WHITE, (flake[0], flake[1]), 3)
        elif self.current_weather == "Heat Wave":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(RED)
            screen.blit(overlay, (0, 0))

    def format_time_of_day(self):
        hours = (self.time_of_day // 100) % 24
        minutes = (self.time_of_day % 100) * 60 // 100
        return f"{hours:02}:{minutes:02}"

    def get_current_season(self):
        month = self.months[self.current_month_index]
        for season, season_months in self.seasons.items():
            if month in season_months:
                return season
        return "spring"  # Default to spring

    def determine_next_weather(self):
        season = self.get_current_season()
        probabilities = self.weather_probabilities[season]
        weather_event = random.choices(list(probabilities.keys()), weights=probabilities.values(), k=1)[0]
        return weather_event

    def current_date(self):
        return f"{self.months[self.current_month_index]} {self.current_day}, {self.current_year}"
