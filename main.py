import requests_toolbelt.adapters.appengine
from flask import Flask, jsonify, request

from decorators.request import authorize
from models.user import User
from services.pinterest import get_batch_of_recipes
from google.appengine.ext import ndb


# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
app = Flask(__name__)


@app.errorhandler(500)
def internal_error(error):

    print "500!!!" + error.message
    return jsonify({'whatev': True})


@app.route('/recipes')
@authorize(token_only=True)
def get_recipe_pins(oauth_token):
    cursor = request.args.get('cursor')
    query = request.args.get('query')
    return jsonify(get_batch_of_recipes(oauth_token, cursor, query))


@app.route('/users/<user_id>')
@authorize(token_only=True)
def create_user(_, user_id):
    User(id=user_id).put()
    return jsonify({})