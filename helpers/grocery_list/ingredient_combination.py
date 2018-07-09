from copy import deepcopy
from fractions import Fraction

from constants.grocery_list import (IGNORED_MINOR_TO_MAJOR, MINOR_TO_MAJOR_CONVERSIONS,
                                    MINOR_VOLUME_WEIGHT_CONVERSIONS, MAJOR_VOLUME_WEIGHT_CONVERSIONS, UNITS, get_pluralizations)
from helpers.grocery_list.fraction_parsing import set_display_amount


def add_ingredient_to_grocery_list(ingredient_to_compare, category, grocery_list, default_units):
    ingredient_to_compare['unit'] = (ingredient_to_compare['unit'] or
                                     default_units.get(ingredient_to_compare['name'], ''))
    original_ingredient_to_compare = deepcopy(ingredient_to_compare)
    for ingredient in grocery_list.get(category, []):
        if do_names_match(ingredient['name'], ingredient_to_compare['name']):
            converted = False
            if ingredient['unit'] != ingredient_to_compare['unit']:
                original_unit = ingredient['unit']
                original_compare_unit = ingredient_to_compare['unit']
                convert_units(ingredient_to_compare)
                convert_units(ingredient)
                converted = (ingredient['unit'] != original_unit) or (ingredient_to_compare['unit']
                                                                      != original_compare_unit)

            if ingredient['unit'] == ingredient_to_compare['unit']:
                ingredient['amount'] = str(Fraction(ingredient_to_compare['amount']) + Fraction(ingredient['amount']))
                if converted:
                    convert_units(ingredient, False)
                set_display_amount(ingredient)
                return
            elif converted:
                convert_units(ingredient, False)
                set_display_amount(ingredient)

    set_display_amount(original_ingredient_to_compare)
    grocery_list.setdefault(category, []).append(original_ingredient_to_compare)


def combine_ingredients(making_recipes):
    grocery_list = {}

    for making_recipe in making_recipes:
        for category, ingredients in making_recipe.metadata.recipe.ingredients.items():
            grocery_list.setdefault(category, [])
            grocery_list[category] += ingredients
    combine_ingredients_across_categories(grocery_list)
    default_units = get_default_units(grocery_list)
    combined_grocery_list = {}
    for category, ingredients in grocery_list.items():
        for ingredient in ingredients:
            add_ingredient_to_grocery_list(ingredient, category, combined_grocery_list, default_units)

    return combined_grocery_list


def combine_ingredients_across_categories(grocery_list):
    ingredient_occurrences = {}
    for category, ingredients in grocery_list.items():
        for ingredient in ingredients:
            ingredient_occurrences.setdefault(ingredient['name'], {})
            ingredient_occurrences[ingredient['name']].setdefault(category, 0)
            ingredient_occurrences[ingredient['name']][category] += 1
    
    for name, categories in ingredient_occurrences.items():
        if len(categories.keys()) > 1:
            max_category = sorted(categories.keys())[0]
            for category, occurrences in categories.items():
                if occurrences > categories[max_category]:
                    max_category = category

            for category in categories.keys():
                if category != max_category:
                    grocery_list[max_category].append(
                        return_and_remove_ingredient_from_category(name, grocery_list[category]))


def return_and_remove_ingredient_from_category(name, category):
    for ingredient in category:
        if ingredient['name'] == name:
            category.remove(ingredient)
            return ingredient


def get_default_units(grocery_list):
    default_units = {}
    unit_occurrences = {}
    for category, ingredients in grocery_list.items():
        for ingredient in ingredients:
            unit_occurrences.setdefault(ingredient['name'], {})
            unit_occurrences[ingredient['name']].setdefault(ingredient['unit'], 0)
            unit_occurrences[ingredient['name']][ingredient['unit']] += 1

    for name, units in unit_occurrences.items():
        if len(units.keys()) > 1:
            max_unit = sorted(units.keys())[0]
            max_occurrences = units[max_unit]
            for unit, occurrences in units.items():
                if occurrences > units[max_unit]:
                    max_unit = unit
                    max_occurrences = occurrences

            if max_occurrences == 1 and not max_unit and len(units.keys()) > 2:
                for unit, occurrences in units.items():
                    if unit:
                        max_unit = unit
                        break
            default_units[name] = max_unit
    return default_units


def convert_units(ingredient, major_to_minor=True):
    if major_to_minor:
        conversion_scale = deepcopy(UNITS)
        weight_scale = MAJOR_VOLUME_WEIGHT_CONVERSIONS
    else:
        conversion_scale = deepcopy(MINOR_TO_MAJOR_CONVERSIONS)
        weight_scale = MINOR_VOLUME_WEIGHT_CONVERSIONS

    conversion_scale.update(get_ingredient_scale(ingredient['name'], weight_scale))

    if not conversion_scale.get(ingredient['unit'], {}).get('conversion'):
        return

    if conversion_scale[ingredient['unit']]['conversion']['unit'] in IGNORED_MINOR_TO_MAJOR and not major_to_minor:
        return

    converted_amount = Fraction(ingredient['amount']) * conversion_scale[ingredient['unit']]['conversion']['ratio']
    if (not major_to_minor and converted_amount.denominator > 8
            and converted_amount.denominator > converted_amount.numerator):
        return

    ingredient['amount'] = str(converted_amount)
    ingredient['unit'] = conversion_scale[ingredient['unit']]['conversion']['unit']

    convert_units(ingredient, major_to_minor)


def get_ingredient_scale(name, scale):
    possible_names = get_pluralizations(name)

    for possible_name in possible_names:
        if scale.get(possible_name):
            return scale.get(possible_name)

    return {}


def do_names_match(name1, name2):
    names1 = get_pluralizations(name1)
    names2 = get_pluralizations(name2)

    for possible_name1 in names1:
        for possible_name2 in names2:
            if possible_name1 == possible_name2:
                return True
    return False
