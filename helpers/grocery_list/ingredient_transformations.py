from constants.grocery_list import IRRELEVANT_INGREDIENTS, UNITS
from helpers.grocery_list.conjunction_parsing import split_conjunctions
from helpers.grocery_list.fraction_parsing import convert_fractions, is_character_part_of_fraction
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
    amount = prepare_for_amount_parsing((ingredient['amount'] or '1'))

    amount_from_amount = get_number_from_string(amount)
    amount_from_name = get_number_from_string(name)

    if amount_from_amount != '1' or amount_from_name == '1':
        transformed_amount = amount_from_amount
        if any(char.isalpha() for char in amount):
            transformed_unit = derive_unit(amount, transformed_amount)
        else:
            transformed_unit = derive_unit(name, amount_from_name)
    else:
        transformed_amount = amount_from_name
        transformed_unit = derive_unit(name, transformed_amount)

    return split_conjunctions(dict(name=name, amount=transformed_amount, unit=transformed_unit))


def prepare_for_amount_parsing(string):
    string = convert_fractions(string)
    string = handle_ranges(string)
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
    all_numbers = ''.join(filter(lambda x: is_character_part_of_fraction(x, string), string)).split() or ['1']
    return all_numbers[1] if all_numbers[0] == '1' and len(all_numbers) > 1 else all_numbers[0]


def derive_unit(string_with_unit, amount):
    words = string_with_unit.split()
    amount_index = 0
    for index, word in enumerate(words):
        if str(amount) in word:
            amount_index = index

    if amount_index == len(words) - 1:
        return ''

    for word in words[amount_index:]:
        if words.index(word) > amount_index and any(char.isdigit() for char in word):
            return ''
        for unit, unit_properties in UNITS.items():
            for synonym in unit_properties['synonyms'] + [unit]:
                if synonym in word:
                    preceding_char, succeeding_char = get_adjacent_characters(word.index(synonym), synonym, word)
                    if is_word_irrelevant_in_context(synonym, preceding_char, succeeding_char):
                        return unit

    return ''
