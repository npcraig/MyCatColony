import random

def generate_random_event(current_cat_count):
    events = ["nothing", "weather_change"]
    if current_cat_count < 15 and random.random() < 0.05:  # 5% chance of a new cat appearing
        events.append("new_cat")
    return random.choice(events)

def handle_random_event(event, create_cat_callback):
    if event == "new_cat":
        create_cat_callback()
        return "A new cat has arrived!"
    elif event == "weather_change":
        return "The weather has changed!"
    return ""
