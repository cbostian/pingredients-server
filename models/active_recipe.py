from google.appengine.ext import ndb


"""
The classes mimic pinterests structure to provide equal structured responses for both recipes from pinterest
and active recipes from our database
"""


class Recipe(ndb.Model):



class Article(ndb.Model):
    description = ndb.StringProperty()
    name = ndb.StringProperty()


class Metadata(ndb.Model):
    article = ndb.structuredProperty(Article)


class Original(ndb.Model):
    url = ndb.StringProperty()
    height = ndb.FloatProperty()
    width = ndb.FloatProperty()


class Image(ndb.Model):
    original = ndb.StructuredProperty(Original)


class ActiveRecipe(ndb.Model):
    note = ndb.StringProperty()
    image = ndb.StructuredProperty(Image)
    original_link = ndb.StringProperty()
    ingredients = ndb.JSONProperty()
    servings = ndb.IntegerProperty()
    board = ndb.StringProperty()