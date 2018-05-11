from google.appengine.ext import ndb


"""
The classes mimic pinterests structure to provide equal structured responses for both recipes from pinterest
and active recipes from our database
"""


class Servings(ndb.Model):
    serves = ndb.FloatProperty()
    yields = ndb.FloatProperty()
    yield_units = ndb.StringProperty()


class Recipe(ndb.Model):
    ingredients = ndb.JsonProperty()


class Article(ndb.Model):
    description = ndb.StringProperty()
    name = ndb.StringProperty()


class Metadata(ndb.Model):
    article = ndb.StructuredProperty(Article)
    recipe = ndb.StructuredProperty(Recipe)
    servings = ndb.StructuredProperty(Servings)


class Original(ndb.Model):
    url = ndb.StringProperty()
    height = ndb.FloatProperty()
    width = ndb.FloatProperty()


class Image(ndb.Model):
    original = ndb.StructuredProperty(Original)


class Board(ndb.Model):
    name = ndb.StringProperty()


class MakingRecipe(ndb.Model):
    id = ndb.StringProperty()
    note = ndb.StringProperty()
    image = ndb.StructuredProperty(Image)
    original_link = ndb.StringProperty()
    metadata = ndb.StructuredProperty(Metadata)
    board = ndb.StructuredProperty(Board)
    making = ndb.BooleanProperty()

    @staticmethod
    def from_dict(recipe_dict):
        return MakingRecipe(
            id=recipe_dict['id'],
            note=recipe_dict.get('note', ''),
            image=Image(
                original=Original(
                    url=recipe_dict.get('image', {}).get('original', {}).get('url', ''),
                    height=recipe_dict.get('image', {}).get('original', {}).get('height', 0.0),
                    width=recipe_dict.get('image', {}).get('original', {}).get('width', 0.0)
                )
            ),
            original_link=recipe_dict.get('original_link', ''),
            metadata=Metadata(
                article=Article(
                    description=recipe_dict.get('metadata', {}).get('article', {}).get('description', ''),
                    name=recipe_dict.get('metadata', {}).get('article', {}).get('name', '')
                ),
                recipe=Recipe(
                    ingredients=recipe_dict.get('metadata', {}).get('recipe', {}).get('ingredients', {})
                ),
                servings=Servings(
                    serves=recipe_dict.get('metadata', {}).get('servings', {}).get('serves'),
                    yields=recipe_dict.get('metadata', {}).get('servings', {}).get('yields'),
                    yield_units=recipe_dict.get('metadata', {}).get('servings', {}).get('yield_units')
                )
            ),
            board=Board(name=recipe_dict.get('board', {}).get('name', '')),
            making=True
        )
