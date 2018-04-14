from flask import Flask, request, abort
from services.pinterest import get_batch_of_recipes
from flask import jsonify
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()
app = Flask(__name__)


def authorize(func):
    def authorized_func():
        oauth_token = request.headers.get('oauth_token')
        if not oauth_token:
            abort(401)
        return func(oauth_token)
    return authorized_func


@app.route('/recipes')
@authorize
def get_recipe_pins(oauth_token):
    cursor = request.args.get('cursor')
    query = request.args.get('query')
    return jsonify(get_batch_of_recipes(oauth_token, cursor, query))
