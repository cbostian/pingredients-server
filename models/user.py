from google.appengine.ext import ndb

from models.active_recipe import ActiveRecipe


class User(ndb.Model):
    active_recipes = ndb.StructuredProperty(ActiveRecipe, repeated=True)
