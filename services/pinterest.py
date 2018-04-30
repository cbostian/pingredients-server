import os
import requests

from copy import deepcopy
from fixtures.recipe_samples import RECIPE_SAMPLES


base_url = 'https://api.pinterest.com/v1'


def get_pins_from_pinterest(oauth_token, cursor, query):
    query_params = {
        'access_token': oauth_token,
        'fields': 'id,note,metadata,image,media,attribution,board,original_link',
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
            ingredients_dict.setdefault(ingredients['category'], []).append(ingredient)

    recipe['ingredients'] = ingredients_dict
    return pin


def filter_recipes_only(pins):
    recipes = []
    for pin in pins:
        if pin.get('metadata', {}).get('recipe'):
            recipes.append(transform_ingredients(pin))
    return recipes


def get_batch_of_recipes(oauth_token, cursor, query):
    if not os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        # dont actually call pinterest in dev because they rate limit us
        return {'data': [transform_ingredients(recipe) for recipe in deepcopy(RECIPE_SAMPLES)], 'cursor': ''}

    pins = []
    while len(pins) < 25:
        pinterest_response = get_pins_from_pinterest(oauth_token, cursor, query)
        pins += filter_recipes_only(pinterest_response['data'])
        cursor = pinterest_response['page']['cursor']
        if not cursor:
            return {'data': pins, 'cursor': cursor}
    return {'data': pins, 'cursor': cursor}
