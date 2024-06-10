class CatCafe:
    def __init__(self):
        self.is_open = False
        self.revenue = 0

    def open_cafe(self):
        self.is_open = True

    def close_cafe(self):
        self.is_open = False

    def earn_revenue(self, amount):
        if self.is_open:
            self.revenue += amount

    def get_revenue(self):
        return self.revenue
