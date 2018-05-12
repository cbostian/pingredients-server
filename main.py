import requests_toolbelt.adapters.appengine
from flask import Flask, jsonify, request
from google.appengine.ext import ndb

from decorators.request import authorize
from models.making_recipe import MakingRecipe
from models.user import User
from services.pinterest import get_batch_of_recipes

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
def activate_recipe(_, user_id):
    user = ndb.Key(User, user_id).get()
    user.making_recipes.append(MakingRecipe.from_dict(request.get_json()))
    user.put()
    return jsonify({})


@app.route('/making-recipes/<recipe_id>', methods=['DELETE'])
@authorize()
def deactivate_recipe(_, user_id, recipe_id):
    user = ndb.Key(User, user_id).get()
    user.making_recipes = [recipe for recipe in user.making_recipes if recipe.id != recipe_id]
    user.put()
    return jsonify({})


# @app.route('/ingredients')
# @authorize()
# def get_ingredients(_, user_id):
#     return jsonify(transform_ingredients(user_id))
