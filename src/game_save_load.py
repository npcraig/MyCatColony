import json
from sprites.cat import Cat
from sprites.shelter import Shelter
from sprites.food import Food
from sprites.water import Water

def save_game(filename, player, cats, shelters, foods, waters, inventory, weather_manager):
    data = {
        'player': {
            'x': player.rect.x,
            'y': player.rect.y
        },
        'cats': [
            {
                'x': cat.rect.x,
                'y': cat.rect.y,
                'health': cat.health,
                'hunger': cat.hunger,
                'thirst': cat.thirst,
                'cleanliness': cat.cleanliness
            } for cat in cats
        ],
        'shelters': [{'x': shelter.rect.x, 'y': shelter.rect.y} for shelter in shelters],
        'foods': [{'x': food.rect.x, 'y': food.rect.y} for food in foods],
        'waters': [{'x': water.rect.x, 'y': water.rect.y} for water in waters],
        'inventory': {
            'food': inventory.food,
            'water': inventory.water,
            'money': inventory.money
        },
        'weather': {
            'time_of_day': weather_manager.time_of_day,
            'current_weather': weather_manager.current_weather,
            'season': weather_manager.season,
            'date': weather_manager.date
        }
    }

    with open(filename, 'w') as file:
        json.dump(data, file)

def load_game(filename, player, cats, shelters, foods, waters, inventory, weather_manager, cat_images, shelter_images, food_image, water_image):
    with open(filename, 'r') as file:
        data = json.load(file)

    player.rect.x = data['player']['x']
    player.rect.y = data['player']['y']

    cats.empty()
    for cat_data in data['cats']:
        cat = Cat(cat_images, shelters)
        cat.rect.x = cat_data['x']
        cat.rect.y = cat_data['y']
        cat.health = cat_data['health']
        cat.hunger = cat_data['hunger']
        cat.thirst = cat_data['thirst']
        cat.cleanliness = cat_data['cleanliness']
        cats.add(cat)

    shelters.empty()
    for shelter_data in data['shelters']:
        shelter = Shelter(shelter_data['x'], shelter_data['y'], shelter_images)
        shelters.add(shelter)

    foods.empty()
    for food_data in data['foods']:
        food = Food(food_data['x'], food_data['y'], food_image)
        foods.add(food)

    waters.empty()
    for water_data in data['waters']:
        water = Water(water_data['x'], water_data['y'], water_image)
        waters.add(water)

    inventory.food = data['inventory']['food']
    inventory.water = data['inventory']['water']
    inventory.money = data['inventory']['money']

    weather_manager.time_of_day = data['weather']['time_of_day']
    weather_manager.current_weather = data['weather']['current_weather']
    weather_manager.season = data['weather']['season']
    weather_manager.date = data['weather']['date']
