class Ingredient():
    def __init__(self, name, amount, unit):
        self.name = name
        self.amount = amount
        self.unit = unit

    def to_dict(self):
        return {
            'name': self.name,
            'amount': self.amount,
            'unit': self.unit,
        }
