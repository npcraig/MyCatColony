class Inventory:
    def __init__(self):
        self.food = 0
        self.water = 0
        self.money = 100  # Start with some money

    def add_food(self, amount):
        self.food += amount

    def add_water(self, amount):
        self.water += amount

    def spend_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def earn_money(self, amount):
        self.money += amount

    def get_status(self):
        return f"Food: {self.food}, Water: {self.water}, Money: ${self.money}"
