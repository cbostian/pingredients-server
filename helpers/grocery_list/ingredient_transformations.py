import re
import unicodedata

from fractions import Fraction
from constants.grocery_list import UNITS, ALL_DERIVED_UNITS
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
        amount = name

    string_with_unit = amount if any(unit in amount for unit in ALL_DERIVED_UNITS) else name

    transformed_amount = max(get_number_from_string(amount), get_number_from_string(name))
    transformed_unit, unit = derive_unit(string_with_unit)

    if transformed_unit and string_with_unit == name:
        if name.index(unit) > (len(name) / 2):
            transformed_name = name[:name.index(unit)].strip()
        else:
            transformed_name = name[name.index(unit) + len(unit):].strip()
    else:
        transformed_name = name

    return split_conjunctions(dict(name=transformed_name, amount=transformed_amount, unit=transformed_unit))


def get_number_from_string(string):
    return float(max((re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?",
                                 convert_fractions(string.replace('-', ' '))) or [0.0])))


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
    min_unit_index = len(string_with_unit)
    derived_unit = original_unit = ''
    for unit, unit_properties in UNITS.items():
        for synonym in unit_properties['synonyms'] + [unit]:
            if ' ' + synonym in string_with_unit:
                unit_index = string_with_unit.index(' ' + synonym)
                if unit_index < min_unit_index:
                    derived_unit = unit
                    original_unit = synonym
                    min_unit_index = unit_index

    return derived_unit, original_unit
