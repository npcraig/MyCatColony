class Achievements:
    def __init__(self):
        self.achievements = {
            "First Cat": False,
            "First Shelter": False,
            "Ten Cats": False,
            "Hundred Dollars": False,
            "Cat Cafe Opened": False,
        }

    def unlock(self, achievement):
        if achievement in self.achievements:
            self.achievements[achievement] = True

    def get_achievements(self):
        return self.achievements

    def get_unlocked(self):
        return [ach for ach, unlocked in self.achievements.items() if unlocked]

    def get_locked(self):
        return [ach for ach, unlocked in self.achievements.items() if not unlocked]
