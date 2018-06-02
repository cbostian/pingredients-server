from models.ingredient import Ingredient


def add_ingredient_to_grocery_list(ingredient_to_compare, category, grocery_list):
    for ingredient in grocery_list.get(category, []):
        if ingredient == ingredient_to_compare:
            ingredient.amount += ingredient_to_compare.amount
            return

    grocery_list.setdefault(category, []).append(ingredient_to_compare)


def combine_ingredients(making_recipes):
    grocery_list = {}

    for making_recipe in making_recipes:
        for category, ingredients in making_recipe.metadata.recipe.ingredients.items():
            grocery_list.setdefault(category, [])
            grocery_list[category] += [Ingredient.from_dict(ingredient) for ingredient in ingredients]

    combine_ingredients_across_categories(grocery_list)

    combined_grocery_list = {}
    for category, ingredients in grocery_list.items():
        for ingredient in ingredients:
            add_ingredient_to_grocery_list(ingredient, category, combined_grocery_list)

    return combined_grocery_list


def combine_ingredients_across_categories(grocery_list):
    ingredient_occurrences = {}
    for category, ingredients in grocery_list.items():
        for ingredient in ingredients:
            ingredient_occurrences.setdefault(ingredient.name, {})
            ingredient_occurrences[ingredient.name].setdefault(category, 0)
            ingredient_occurrences[ingredient.name][category] += 1
    
    for name, categories in ingredient_occurrences.items():
        if len(categories.keys()) > 1:
            max_category = categories.keys()[0]
            for category, occurrences in categories.items():
                if occurrences > categories[max_category]:
                    max_category = category

            for category in categories.keys():
                if category != max_category:
                    grocery_list[max_category].append(
                        return_and_remove_ingredient_from_category(name, grocery_list[category]))


def return_and_remove_ingredient_from_category(name, category):
    for ingredient in category:
        if ingredient.name == name:
            category.remove(ingredient)
            return ingredient
