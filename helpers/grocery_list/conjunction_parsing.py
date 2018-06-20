from fractions import Fraction

from constants.grocery_list import ADDITIVE_CONJUNCTIONS, CONDITIONAL_CONJUNCTIONS, EXCLUSIVE_CONJUNCTIONS, UNITS
from helpers.grocery_list.name_sanitization import sanitize_name


def split_conjunctions(ingredient):
    ingredient['name'] = remove_conditional_conjunctions(ingredient['name'])
    ingredients = [ingredient]
    for conjunction in ADDITIVE_CONJUNCTIONS + EXCLUSIVE_CONJUNCTIONS:
        contextual_conjunction = get_contextual_conjunction(conjunction)
        if (contextual_conjunction not in ingredient['name'] or
                is_conjunction_between_numbers(conjunction, ingredient['name'])):
            continue

        words = split_words_on_conjunction(contextual_conjunction, ingredient['name'])
        if conjunction in ADDITIVE_CONJUNCTIONS:
            ingredients.append(split_additive_conjunctions(ingredient, words, conjunction))
        else:
            if is_conjunction_between_amount(conjunction, ingredient['name']):
                for word in words:
                    if word.isdigit() or word in UNITS.keys() or word == conjunction:
                        ingredient['name'] = ingredient['name'].replace(word, '')
            else:
                ingredient['name'] = sanitize_name(split_exclusive_conjunctions(words, conjunction))
    ingredient['name'] = sanitize_name([ingredient['name']])
    return ingredients


def remove_conditional_conjunctions(name):
    for conditional_conjunction in CONDITIONAL_CONJUNCTIONS:
        conditional_conjunction = ' ' + conditional_conjunction
        if conditional_conjunction in name:
            conditional_index = name.index(conditional_conjunction)
            terminal_index = len(name)
            for conjunction in filter(lambda c: len(c) > 1 , ADDITIVE_CONJUNCTIONS + EXCLUSIVE_CONJUNCTIONS):
                contextual_conjunction = get_contextual_conjunction(conjunction)
                if contextual_conjunction in name[conditional_index:]:
                    conjunction_index = name.find(contextual_conjunction, conditional_index)
                    if 0 <= conjunction_index < terminal_index:
                        terminal_index = conjunction_index
            name = name.replace(name[conditional_index:terminal_index], '')

    return name


def split_exclusive_conjunctions(words, conjunction):
    left = words[:words.index(conjunction)]
    right = words[words.index(conjunction) + 1:]
    if len(left) > len(right):
        return [' '.join(left)]
    elif len(right) > len(left):
        return [' '.join(right)]

    return [' '.join(left), ' '.join(right)]


def split_additive_conjunctions(ingredient, words, conjunction):
    left_name = ' '.join(words[:words.index(conjunction)])
    right_name = ' '.join(words[words.index(conjunction) + 1:])
    if ',' in left_name:
        _, primary_noun_index = get_closest_to_character(',', left_name, False, lambda char: char.isspace())
        right_name = left_name[primary_noun_index:left_name.index(',')] + ' ' + right_name
    elif ',' in right_name:
        _, primary_noun_index = get_closest_to_character(', ', right_name, True, lambda char: char.isspace())
        left_name += ' ' + right_name[right_name.index(', ') + 2:primary_noun_index + 1]

    halved_amount = str(Fraction(ingredient['amount']) / 2)
    ingredient['amount'] = halved_amount
    ingredient['name'] = sanitize_name([left_name])

    return {
        'amount': halved_amount,
        'name': sanitize_name([right_name]),
        'unit': ingredient['unit']
    }


def is_conjunction_between_numbers(conjunction, string):
    left, _ = get_closest_to_character(conjunction, string, False)
    right, _ = get_closest_to_character(conjunction, string, True)
    return left.isdigit() and right.isdigit()


def get_closest_to_character(character, string, incrementing, condition=lambda char: not char.isspace()):
    closest_index = (string.index(character) + (1 if incrementing else -1) +
                     (len(character) if len(character) > 1 and incrementing else 0))
    closest = string[closest_index]
    while not condition(closest) and (closest_index < (len(string) - 1) if incrementing else closest_index > 0):
        closest_index += 1 if incrementing else -1
        closest = string[closest_index]

    return closest, closest_index


def is_conjunction_between_amount(conjunction, string):
    words = split_words_on_conjunction(conjunction, string)
    conjunction_index = words.index(conjunction.strip())

    return (words[conjunction_index - 1].isdigit()
            or words[conjunction_index + conjunction_index < len(words) - 1].isdigit())


def split_words_on_conjunction(contextual_conjunction, string):
    return string.replace(contextual_conjunction, ' ' + contextual_conjunction + ' ').split()


def get_contextual_conjunction(conjunction):
    return (' ' if len(conjunction) > 1 else '') + conjunction
