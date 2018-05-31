from difflib import SequenceMatcher

from helpers.grocery_list.ingredient_synonyms import INGREDIENT_COMMON_ADJECTIVES


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

    @staticmethod
    def from_dict(dict):
        return Ingredient(name=dict.get('name', ''), amount=float(dict.get('amount', 0.0)), unit=dict.get('unit', ''))

    def valid_names_sorted(self):
        valid_names = [''.join(sorted(self.name.lower().split(' ')))]
        for adjective in INGREDIENT_COMMON_ADJECTIVES.get(self.name, {}).get('common_adjectives', []):
            valid_names.append(''.join(sorted((self.name.lower() + ' ' + adjective).split(' '))))
        return valid_names

    def __eq__(self, other):
        return self.do_names_match(other) and self.unit == other.unit

    def do_names_match(self, other):
        for self_valid_name in self.valid_names_sorted():
            for other_valid_name in other.valid_names_sorted():
                if SequenceMatcher(None, self_valid_name, other_valid_name).ratio() > 0.7857142857142856:
                    return True
