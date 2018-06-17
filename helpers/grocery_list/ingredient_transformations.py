import re
import unicodedata

from fractions import Fraction
from constants.grocery_list import IRRELEVANT_INGREDIENTS, UNITS
from helpers.grocery_list.conjunction_parsing import split_conjunctions, is_conjunction_between_numbers
from helpers.grocery_list.name_sanitization import get_adjacent_characters, is_word_irrelevant_in_context


def transform_ingredients(pin):
    ingredients_dict = {}
    recipe = pin['metadata']['recipe']

    if not recipe.get('ingredients', []):
        return pin

    for ingredients in recipe['ingredients']:
        for ingredient in ingredients.get('ingredients', []):
            ingredients_dict.setdefault(ingredients['category'], [])
            if ingredient['name'].lower() not in IRRELEVANT_INGREDIENTS:
                transformed_ingredients = transform_ingredient(ingredient)
                for transformed_ingredient in transformed_ingredients:
                    if transformed_ingredient['name'].lower() not in IRRELEVANT_INGREDIENTS:
                        ingredients_dict[ingredients['category']].append(transformed_ingredient)

    recipe['ingredients'] = ingredients_dict
    return pin


def transform_ingredient(ingredient):
    name = prepare_for_amount_parsing(ingredient['name'])
    amount = prepare_for_amount_parsing((ingredient['amount'] or '1.0'))

    amount_from_amount = get_number_from_string(amount)
    amount_from_name = get_number_from_string(name)

    if amount_from_amount != 1 or amount_from_name == 1:
        transformed_amount = amount_from_amount
        transformed_unit = derive_unit(amount, transformed_amount)
    else:
        transformed_amount = amount_from_name
        transformed_unit = derive_unit(name, transformed_amount)

    return split_conjunctions(dict(name=name, amount=transformed_amount, unit=transformed_unit))


def prepare_for_amount_parsing(string):
    string = convert_fractions(string)
    string = handle_ranges(string)
    string = make_all_numbers_floats(string)
    return string


def handle_ranges(string):
    string = string.replace('-', ' - ')
    words = string.split()
    try:
        range_index = words.index('-')
        left = words[range_index - 1 if range_index > 0 else 0]
        right = words[range_index + 1 if range_index < len(words) - 1 else 0]
        if filter(lambda char: char.isdigit(), left) and filter(lambda char: char.isdigit(), right):
            string = string.replace(left, '')
            string = string.replace('-', '')
        return string
    except ValueError:
        return string


def make_all_numbers_floats(string):
    all_numbers = find_all_numbers(string)
    for number in all_numbers:
        clean_number = filter(lambda char: char.isdigit(), number)
        clean_number_indices = filter(lambda idx: not is_number_part_of_other_number(idx, clean_number, string),
                                      [match.start() for match in re.finditer(clean_number, string)])
        while bool(clean_number_indices):
            index = clean_number_indices.pop(0)
            string = string[:index] + str(float(clean_number)) + string[index + len(clean_number):]
            clean_number_indices = filter(lambda idx: not is_number_part_of_other_number(idx, clean_number, string),
                                          [match.start() for match in re.finditer(clean_number, string)])
    return string


def is_number_part_of_other_number(number_index, number, string):
    is_preceding_part_of_number = False
    is_succeeding_part_of_number = False

    if number_index > 0:
        is_preceding_part_of_number = string[number_index - 1].isdigit() or string[number_index - 1] == '.'

    if number_index + len(number) < len(string):
        is_succeeding_part_of_number = string[number_index + len(number)].isdigit() or (
                string[number_index + len(number)] == '.' and (number_index + len(number)) < (len(string) - 1))

    return is_preceding_part_of_number or is_succeeding_part_of_number


def get_number_from_string(string):
    all_numbers = find_all_numbers(string)
    return float(all_numbers[1] if float(all_numbers[0]) == 1 and len(all_numbers) > 1 else all_numbers[0])


def find_all_numbers(string):
    return re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", string) or ['1.0']


def convert_fractions(string_to_convert):
    fraction = ''.join(filter(lambda x: is_character_part_of_fraction(x, string_to_convert), string_to_convert)).strip()
    if not fraction or '/' not in string_to_convert:
        return string_to_convert
    transformed_fraction = str(float(sum(Fraction(num) for num in fraction.split())))
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


def derive_unit(string_with_unit, amount):
    words = string_with_unit.split()
    amount_index = 0
    for index, word in enumerate(words):
        if str(amount) in word:
            amount_index = index

    if amount_index == len(words) - 1:
        return ''

    for unit, unit_properties in UNITS.items():
        for synonym in unit_properties['synonyms'] + [unit]:
            for word in words[amount_index + 1:]:
                if synonym in word:
                    preceding_char, succeeding_char = get_adjacent_characters(word.index(synonym), word, word)
                    if is_word_irrelevant_in_context(synonym, preceding_char, succeeding_char):
                        return unit

    return ''
