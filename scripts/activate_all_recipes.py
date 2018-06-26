import requests
import json

from grocery_list_response import EXPECTED_GROCERY_LIST


def test_grocery_list():
    response = requests.get('http://localhost:8080/grocery-list', headers={'oauth_token': '123', 'user_id': 'dev_user_id'}).json()
    compare_groceries(EXPECTED_GROCERY_LIST, response)


def compare_groceries(expected_grocery_list, actual_grocery_list):
    for expected_category, expected_ingredients in expected_grocery_list.items():
        for expected_ingredient in expected_ingredients:
            match = False
            for actual_ingredient in actual_grocery_list[expected_category]:
                if (actual_ingredient['name'] ==  expected_ingredient['name'] and
                        actual_ingredient['amount'] == expected_ingredient['amount'] and
                        actual_ingredient['unit'] == expected_ingredient['unit']):
                    match = True
                    break
            if not match:
                print expected_ingredient
            assert match


all_recipes = requests.get('http://localhost:8080/recipes', headers={'oauth_token': '123', 'user_id': 'dev_user_id'}).json()['data']

for recipe in all_recipes:
    requests.delete('http://localhost:8080/making-recipes/' + recipe['id'], headers={'oauth_token': '123', 'user_id': 'dev_user_id'})
    requests.post('http://localhost:8080/making-recipes', data=json.dumps(recipe), headers={'oauth_token': '123', 'user_id': 'dev_user_id', 'Content-Type': 'application/json'})

test_grocery_list()
