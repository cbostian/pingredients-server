import re
import unicodedata

from fractions import Fraction
from constants.grocery_list import VALID_UNITS
from helpers.grocery_list.conjunction_parsing import split_conjunctions, is_conjunction_between_numbers


def transform_ingredients(pin):
    ingredients_dict = {}
    recipe = pin['metadata']['recipe']

    if not recipe.get('ingredients', []):
        return pin

    for ingredients in recipe['ingredients']:
        for ingredient in ingredients.get('ingredients', []):
            ingredients_dict.setdefault(ingredients['category'], [])
            ingredients_dict[ingredients['category']] += transform_ingredient(ingredient)

    recipe['ingredients'] = ingredients_dict
    return pin


def transform_ingredient(ingredient):
    name = ingredient['name']
    amount = ingredient['amount'] or ''
    if not amount:
        name = convert_fractions(name)
        amount = name
    else:
        amount = convert_fractions(amount)

    string_with_unit = amount
    for numeric_conversion in [float, int]:
        try:
            numeric_conversion(amount)
            string_with_unit = name
        except ValueError:
            pass

    transformed_amount = float((re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", amount) or [0.0])[0])
    transformed_unit = derive_unit(string_with_unit)
    if transformed_unit and string_with_unit == name:
        if name.index(transformed_unit) > (len(name) / 2):
            transformed_name = name[:name.index(transformed_unit)].strip()
        else:
            transformed_name = name[name.index(transformed_unit) + len(transformed_unit):].strip()
    else:
        transformed_name = name
    return split_conjunctions(dict(name=transformed_name, amount=transformed_amount, unit=transformed_unit))


def convert_fractions(string_to_convert):
    fraction = ''.join(filter(lambda x: is_character_part_of_fraction(x, string_to_convert), string_to_convert)).strip()
    if not fraction:
        return string_to_convert
    transformed_fraction = repr(float(sum(Fraction(num) for num in fraction.split())))
    return convert_unicode_fractions(string_to_convert.replace(fraction, transformed_fraction))


def is_character_part_of_fraction(character, string):
    return (character.isdigit() or (character == '/' and is_conjunction_between_numbers('/', string))
            or character.isspace())


def convert_unicode_fractions(string_to_convert):
    unicode_string = string_to_convert.decode('unicode-escape')
    unicode_fraction = filter(lambda x: unicodedata.name(x).startswith('VULGAR FRACTION'), unicode_string)
    if unicode_fraction:
        string_to_convert = unicode_string.replace(unicode_fraction, str(unicodedata.numeric(unicode_fraction)))
    return str(string_to_convert)


def derive_unit(string_with_unit):
    return (filter(string_with_unit.split().__contains__, VALID_UNITS) or [''])[0]
