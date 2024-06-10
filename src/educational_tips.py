class EducationalTips:
    def __init__(self):
        self.tips = [
            "Spaying and neutering your cats helps control the population and improve their health.",
            "Regular vet visits are important to ensure the well-being of your cats.",
            "Providing shelters protects cats from harsh weather conditions.",
            "Cats need a balanced diet to stay healthy and active.",
            "Toys and enrichment activities keep your cats entertained and happy."
        ]
        self.current_tip_index = 0

    def get_current_tip(self):
        return self.tips[self.current_tip_index]

    def next_tip(self):
        self.current_tip_index = (self.current_tip_index + 1) % len(self.tips)
