import os
import re
import requests
import unicodedata

from copy import deepcopy
from fractions import Fraction
from fixtures.recipe_samples import RECIPE_SAMPLES
from models.ingredient import Ingredient


base_url = 'https://api.pinterest.com/v1'


def get_pins_from_pinterest(oauth_token, cursor, query):
    query_params = {
        'access_token': oauth_token,
        'fields': 'id,note,metadata,image,board,original_link',
        'limit': 100
    }

    if query:
        request_url = base_url + '/me/search/pins/'
        query_params.update({
            'query': query
        })
    else:
        request_url = base_url + '/me/pins/'

    if cursor:
        query_params.update({
            'cursor': cursor
        })

    response = requests.get(request_url, params=query_params)

    return response.json()


def transform_ingredients(pin):
    ingredients_dict = {}
    recipe = pin['metadata']['recipe']

    if not recipe.get('ingredients', []):
        return pin

    for ingredients in recipe['ingredients']:
        for ingredient in ingredients.get('ingredients', []):
            ingredients_dict.setdefault(ingredients['category'], []).append(transform_ingredient(ingredient))

    recipe['ingredients'] = ingredients_dict
    return pin


def transform_ingredient(ingredient):
    amount = convert_fraction(ingredient['amount'] or '')
    name = ingredient['name']
    string_with_unit = amount
    if not amount or amount.isdigit():
        string_with_unit = name

    transformed_amount = (re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", amount) or [0.0])[0]
    transformed_unit = derive_unit(string_with_unit)
    transformed_name = name[:name.index(transformed_unit)].strip() if (transformed_unit and
                                                                       string_with_unit == name) else name

    return dict(name=transformed_name, amount=transformed_amount, unit=transformed_unit)


def convert_fraction(string_to_convert):
    fraction = ''.join(filter(lambda x: x.isdigit() or x == '/' or x.isspace(), string_to_convert)).strip()
    transformed_fraction = repr(float(sum(Fraction(num) for num in fraction.split())))
    new_string = string_to_convert.replace(fraction, transformed_fraction)
    return new_string


def derive_unit(string_with_unit):
    valid_units = ['oz', 'ounce', 'lb', 'tsp', 'teaspoon', 'cup', 'dash', 'jar', 'tbsp', 'tablespoon', 'ml', 'g',
                   'head', 'can', 'clove']

    return (filter(string_with_unit.split().__contains__, valid_units) or [''])[0]


def transform_servings(pin):
    servings = pin['metadata']['recipe']['servings']

    if not servings.get('serves') and not servings.get('yields'):
        return pin

    if servings.get('serves'):
        if servings.get('serves').find('-') > -1:
            pin['metadata']['recipe']['servings'] = {'serves': sum(map(float, servings.get('serves').split('-')))/2}
        else:
            pin['metadata']['recipe']['servings'] = {'serves': float(servings.get('serves', ''))}

        return pin

    yields = float(''.join(filter(str.isdigit, servings.get('yields'))))
    yield_units = ''.join(filter(lambda x: str.isalpha(x) or str.isspace(x),
                                 servings.get('summary'))).replace('Makes', '').strip()

    pin['metadata']['recipe']['servings'] = {'yields': yields, 'yield_units': yield_units}

    return pin


def transform_making(pin, making_recipes):
    pin['making'] = False
    if any(recipe.id == pin['id'] for recipe in making_recipes):
        pin['making'] = True

    return pin


def transform(pin, making_recipes):
    transform_servings(pin)
    transform_ingredients(pin)
    transform_making(pin, making_recipes)
    return pin


def filter_recipes_only(pins, making_recipes):
    recipes = []
    for pin in pins:
        if pin.get('metadata', {}).get('recipe'):
            recipes.append(transform(pin, making_recipes))
    return recipes


def get_batch_of_recipes(oauth_token, cursor, query, making_recipes):
    if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # dont actually call pinterest in dev because they rate limit us
        return {'data': [transform(recipe, making_recipes) for recipe in deepcopy(RECIPE_SAMPLES)], 'cursor': ''}

    pins = []
    while len(pins) < 25:
        pinterest_response = get_pins_from_pinterest(oauth_token, cursor, query)
        pins += filter_recipes_only(pinterest_response['data'], making_recipes)
        cursor = pinterest_response['page']['cursor']
        if not cursor:
            return {'data': pins, 'cursor': cursor}
    return {'data': pins, 'cursor': cursor}
