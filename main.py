import requests_toolbelt.adapters.appengine
from flask import Flask, jsonify, request
from google.appengine.ext import ndb

from decorators.request import authorize
from models.active_recipe import ActiveRecipe
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
def get_recipe_pins(oauth_token, _):
    cursor = request.args.get('cursor')
    query = request.args.get('query')
    return jsonify(get_batch_of_recipes(oauth_token, cursor, query))


@app.route('/users/<user_id>', methods=['PUT'])
@authorize(token_only=True)
def create_user(_, user_id):
    User(id=user_id).put()
    return jsonify({})


@app.route('/activate-recipe', methods=['POST'])
@authorize()
def activate_recipe(_, user_id):
    user = ndb.Key(User, user_id).get()
    user.active_recipes.append(ActiveRecipe.from_dict(request.get_json()))
    user.put()
    return jsonify({})
