import json
import re

from google.appengine.ext import ndb
from fractions import Fraction
from models.user import User
from models.ingredient import Ingredient


def get_making_recipes(user_id):
    user = ndb.Key(User, user_id).get()
    return user.making_recipes



