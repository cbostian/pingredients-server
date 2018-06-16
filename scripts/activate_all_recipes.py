import requests
import json


all_recipes = requests.get('http://localhost:8080/recipes', headers={'oauth_token': '123', 'user_id': 'dev_user_id'}).json()['data']

for recipe in all_recipes:
    requests.delete('http://localhost:8080/making-recipes/' + recipe['id'], headers={'oauth_token': '123', 'user_id': 'dev_user_id'})
    requests.post('http://localhost:8080/making-recipes', data=json.dumps(recipe), headers={'oauth_token': '123', 'user_id': 'dev_user_id', 'Content-Type': 'application/json'})