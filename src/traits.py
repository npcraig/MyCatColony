import random

# Define possible traits
FUR_COLORS = ["Black", "White", "Brown", "Orange", "Gray", "Calico"]
EYE_COLORS = ["Blue", "Green", "Yellow", "Brown"]
BEHAVIORS = ["Active", "Lazy", "Curious", "Timid"]
BREEDS = ["Siamese", "Persian", "Maine Coon", "Ragdoll", "Sphynx", "Bengal"]

# Define possible names
NAMES = ["Whiskers", "Shadow", "Luna", "Simba", "Bella", "Oliver", "Milo", "Nala", "Leo", "Cleo"]

def generate_random_traits():
    return {
        "fur_color": random.choice(FUR_COLORS),
        "eye_color": random.choice(EYE_COLORS),
        "behavior": random.choice(BEHAVIORS),
        "breed": random.choice(BREEDS),
    }

def generate_random_name():
    return random.choice(NAMES)

def inherit_traits(parent1_traits, parent2_traits):
    return {
        "fur_color": random.choice([parent1_traits["fur_color"], parent2_traits["fur_color"]]),
        "eye_color": random.choice([parent1_traits["eye_color"], parent2_traits["eye_color"]]),
        "behavior": random.choice([parent1_traits["behavior"], parent2_traits["behavior"]]),
        "breed": random.choice([parent1_traits["breed"], parent2_traits["breed"]]),
    }

def apply_random_mutation(traits):
    if random.random() < 0.1:  # 10% chance of mutation
        traits["fur_color"] = random.choice(FUR_COLORS)
    if random.random() < 0.1:  # 10% chance of mutation
        traits["eye_color"] = random.choice(EYE_COLORS)
    if random.random() < 0.1:  # 10% chance of mutation
        traits["behavior"] = random.choice(BEHAVIORS)
    if random.random() < 0.1:  # 10% chance of mutation
        traits["breed"] = random.choice(BREEDS)
    return traits
