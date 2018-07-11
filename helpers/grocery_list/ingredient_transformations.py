from constants.grocery_list import HOMONYM_UNITS, IRRELEVANT_INGREDIENTS, UNITS
from helpers.grocery_list.conjunction_parsing import split_conjunctions
from helpers.grocery_list.name_sanitization import get_adjacent_characters, is_word_irrelevant_in_context
from helpers.grocery_list.number_parsing import prepare_for_amount_parsing, get_number_from_string


def transform_ingredients_structure(pin):
    ingredients_dict = {}
    recipe = pin['metadata']['recipe']

    if not recipe.get('ingredients', []):
        return pin

    for ingredients in recipe['ingredients']:
        for ingredient in ingredients.get('ingredients', []):
            ingredients_dict.setdefault(ingredients['category'], [])
            ingredients_dict[ingredients['category']].append(ingredient)

    recipe['ingredients'] = ingredients_dict
    return pin


def transform_ingredients(pin):
    recipe = pin['metadata']['recipe']
    new_ingredients = {}
    for category, ingredients in recipe['ingredients'].items():
        new_ingredients.setdefault(category, [])
        for ingredient in ingredients:
            if ingredient['name'].lower() not in IRRELEVANT_INGREDIENTS:
                transformed_ingredients = transform_ingredient(ingredient)
                for transformed_ingredient in transformed_ingredients:
                    if transformed_ingredient['name'].lower() not in IRRELEVANT_INGREDIENTS:
                        new_ingredients[category].append(transformed_ingredient)

    recipe['ingredients'] = new_ingredients
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

    if transformed_unit in HOMONYM_UNITS:
        name = name.replace(transformed_unit + 's', ' ').replace(transformed_unit, ' ')

    return split_conjunctions(dict(name=name.replace(transformed_amount, ' '), amount=transformed_amount,
                                   unit=transformed_unit))


def derive_unit(string_with_unit, amount):
    words = string_with_unit.split()
    amount_index = 0
    for index, word in enumerate(words):
        if str(amount) in word:
            amount_index = index

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
