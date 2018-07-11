import os
import requests

from copy import deepcopy
from fixtures.recipe_samples import RECIPE_SAMPLES
from helpers.grocery_list.ingredient_transformations import transform_ingredients_structure


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

    yields = servings.get('yields', '').encode('ascii', 'ignore')
    summary = servings.get('summary', '').encode('ascii', 'ignore')

    yields = float(''.join(filter(str.isdigit, yields)))
    yield_units = ''.join(filter(lambda x: str.isalpha(x) or str.isspace(x), summary)).replace('Makes', '').strip()

    pin['metadata']['recipe']['servings'] = {'yields': yields, 'yield_units': yield_units}

    return pin


def transform_making(pin, making_recipes):
    pin['making'] = False
    if any(recipe.id == pin['id'] for recipe in making_recipes):
        pin['making'] = True

    return pin


def transform(pin, making_recipes):
    transform_servings(pin)
    transform_ingredients_structure(pin)
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
