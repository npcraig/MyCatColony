# random_events.py
import random

def generate_random_event():
    events = ["new_cat", "weather_change"]
    return random.choice(events)

def handle_random_event(event, create_cat_callback):
    if event == "new_cat":
        create_cat_callback()
        return "A new cat has arrived!"
    elif event == "weather_change":
        return "The weather has changed!"
    return ""
