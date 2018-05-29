import requests_toolbelt.adapters.appengine
from flask import Flask, jsonify, request
from google.appengine.ext import ndb

from decorators.request import authorize
from models.ingredient import Ingredient
from models.making_recipe import MakingRecipe
from models.user import User
from services.pinterest import get_batch_of_recipes
import json

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):
    print error.message


@app.route('/recipes')
@authorize()
def get_recipe_pins(oauth_token, user_id):
    cursor = request.args.get('cursor')
    query = request.args.get('query')
    return jsonify(get_batch_of_recipes(oauth_token, cursor, query, ndb.Key(User, user_id).get().making_recipes))


@app.route('/users/<user_id>', methods=['PUT'])
@authorize(token_only=True)
def create_user(_, user_id):
    User.get_or_insert(user_id)
    return jsonify({})


@app.route('/making-recipes', methods=['POST'])
@authorize()
def make_recipe(_, user_id):
    user = ndb.Key(User, user_id).get()
    user.making_recipes.append(MakingRecipe.from_dict(request.get_json()))
    user.put()
    return jsonify({})


@app.route('/making-recipes')
@authorize()
def get_making_recipes(_, user_id):
    return jsonify({'data': ndb.Key(User, user_id).get().to_dict().get('making_recipes', [])})


@app.route('/making-recipes/<recipe_id>', methods=['DELETE'])
@authorize()
def unmake_recipe(_, user_id, recipe_id):
    user = ndb.Key(User, user_id).get()
    user.making_recipes = [recipe for recipe in user.making_recipes if recipe.id != recipe_id]
    user.put()
    return jsonify({})


@app.route('/grocery-list')
@authorize()
def get_groceries(_, user_id):
    making_recipes = ndb.Key(User, user_id).get().making_recipes
    grocery_list = {}

    def add_ingredient_to_grocery_list(ingredient_to_compare, category):
        for ingredient in grocery_list.get(category, []):
            if ingredient == ingredient_to_compare:
                try:
                    ingredient.amount += ingredient_to_compare.amount
                except:
                    print ingredient.to_dict()
                    print '\n'
                    print ingredient_to_compare.to_dict()
                    print '\n'
                return
        grocery_list.setdefault(category, []).append(ingredient_to_compare)

    for making_recipe in making_recipes:
        for category, ingredients in making_recipe.metadata.recipe.ingredients.items():
            for ingredient in ingredients:
                add_ingredient_to_grocery_list(Ingredient.from_dict(ingredient), category)

    return jsonify({category: map(lambda ingredient: ingredient.to_dict(), ingredients)
                    for category, ingredients in grocery_list.items()})
