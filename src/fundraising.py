import pygame
import random

class FundraisingEvent:
    def __init__(self, name, duration, earning_rate):
        self.name = name
        self.duration = duration  # in seconds
        self.earning_rate = earning_rate  # money earned per second
        self.elapsed_time = 0

    def update(self, delta_time):
        self.elapsed_time += delta_time
        return self.earning_rate * delta_time if self.elapsed_time < self.duration else 0

class Fundraising:
    def __init__(self):
        self.active_events = []
        self.funds = 0

    def start_event(self, event):
        self.active_events.append(event)

    def update_events(self, delta_time):
        for event in self.active_events:
            self.funds += event.update(delta_time)
        self.active_events = [event for event in self.active_events if event.elapsed_time < event.duration]

    def get_funds(self):
        return self.funds

    def spend_funds(self, amount):
        if self.funds >= amount:
            self.funds -= amount
            return True
        return False
