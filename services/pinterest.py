import os
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
            ingredients_dict.setdefault(ingredients['category'], []).append(transform_ingredient(ingredient).to_dict())

    recipe['ingredients'] = ingredients_dict
    return pin


def transform_unicode_and_fractions(string):
    try:
        fraction = ''.join(
            filter(lambda x: str.isdigit(x) or x == '/' or str.isspace(x), string)).strip()
        transformed_fraction = str(float(sum(Fraction(num) for num in fraction.split())))
        string.replace(fraction, transformed_fraction)
    except:
        pass
    try:
        unicode_fraction = filter(
            lambda x: unicodedata.name(x).startswith('VULGAR FRACTION'), string.decode('unicode-escape'))
        transformed_unicode = str(unicodedata.numeric(unicode_fraction))
        string.decode('unicode-escape').replace(unicode_fraction, transformed_unicode).encode('utf-8')
    except:
        pass
    return string


def transform_ingredient(ingredient):
    amount = ingredient['amount']
    name = ingredient['name'].decode('unicode-escape')
    if amount.isdigit() and name.isalpha():
        transformed_amount = amount
        transformed_unit = ''
        transformed_name = name
    else:
        measurement_array = ['oz', 'ounces', 'lb', 'lbs', 'tsp', 'teaspoon', 'cup', 'dash', 'jar',
                             'cups', 'tbsp', 'tablespoon', 'ml', 'g', 'head', 'heads', 'can', 'cans', 'cloves']
        measure_list = filter(amount.split().__contains__, measurement_array)
        if len(measure_list) == 1:
            if amount[:amount.index(measure_list[0])].isdigit() and not amount[(
                    amount.index(measure_list[0]) + len(measure_list[0])):]:
                transformed_amount = amount[:amount.index(measure_list[0])]
                transformed_unit = measure_list[0]
                transformed_name = name
        else:
            measure_indices = dict()
            for measure in measure_list:
                measure_indices[measure] = measure_indices[measure].append(
                    amount[:amount.index(measure)], amount[amount.index(measure) + len(measure):])

    return Ingredient(name=transformed_name, amount=transformed_amount, unit=transformed_unit)


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
