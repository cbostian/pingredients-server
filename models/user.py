from google.appengine.ext import ndb

from models.making_recipe import MakingRecipe


class User(ndb.Model):
    making_recipes = ndb.StructuredProperty(MakingRecipe, repeated=True)
