import random
from sprites.cat import Cat

def generate_random_event(num_cats):
    events = ["new_cat", "lost_cat", "weather_change"]
    weights = [1, 1, 8]  # Make new cats and lost cats rare
    if num_cats >= 15:
        weights[0] = 0  # No more new cats if there are 15 or more
    event = random.choices(events, weights=weights, k=1)[0]
    return event

def handle_random_event(event, create_new_cat):
    if event == "new_cat":
        create_new_cat()
        return "A new cat has joined the colony!"
    elif event == "lost_cat":
        # Implement logic for losing a cat
        return "A cat has left the colony."
    elif event == "weather_change":
        # Implement logic for changing the weather
        return "The weather has changed."
    return ""
