from fractions import Fraction

from constants.grocery_list import (ADDITIVE_CONJUNCTIONS, CONDITIONAL_CONJUNCTIONS, EXCLUSIVE_CONJUNCTIONS,
                                    IGNORED_CONJUNCTION_INGREDIENTS, IRRELEVANT_INGREDIENTS, UNITS)
from helpers.grocery_list.name_sanitization import sanitize_name, remove_irrelevant_phrases
from helpers.grocery_list.number_parsing import get_number_from_string, get_closest_to_character
from helpers.grocery_list.text_parsing import is_word_between_numbers


def split_conjunctions(ingredient):
    ingredient['name'] = remove_irrelevant_phrases(remove_conditional_conjunctions(ingredient['name'].lower()))
    ingredients = [ingredient]
    for conjunction in ADDITIVE_CONJUNCTIONS + EXCLUSIVE_CONJUNCTIONS:
        contextual_conjunction = get_contextual_conjunction(conjunction, ingredient['name'])
        if contextual_conjunction not in ingredient['name']:
            continue
        if is_word_between_numbers(conjunction, ingredient['name']):
            ingredient['name'] = ingredient['name'].replace(conjunction, ' ')
            continue

        words = split_words_on_conjunction(contextual_conjunction, ingredient['name'])
        if conjunction in ADDITIVE_CONJUNCTIONS:
            split_ingredient = split_additive_conjunctions(ingredient, words, contextual_conjunction)
            if split_ingredient:
                ingredients += split_conjunctions(split_ingredient)
        else:
            if is_conjunction_between_amount(conjunction, ingredient['name']):
                for word in words:
                    if word.isdigit() or word in UNITS.keys() or word == conjunction:
                        ingredient['name'] = ingredient['name'].replace(word, '')
            else:
                ingredient['name'] = sanitize_name(split_exclusive_conjunctions(words, contextual_conjunction))
                split_conjunctions(ingredient)

    ingredient['name'] = sanitize_name([ingredient['name']])
    return ingredients


def remove_conditional_conjunctions(name):
    for conditional_conjunction in CONDITIONAL_CONJUNCTIONS:
        conditional_conjunction = ' ' + conditional_conjunction
        if conditional_conjunction in name:
            conditional_index = name.index(conditional_conjunction)
            terminal_index = len(name)
            for conjunction in filter(lambda c: len(c) > 1, ADDITIVE_CONJUNCTIONS + EXCLUSIVE_CONJUNCTIONS):
                contextual_conjunction = get_contextual_conjunction(conjunction, name)
                if contextual_conjunction in name[conditional_index:]:
                    conjunction_index = name.find(contextual_conjunction, conditional_index)
                    if 0 <= conjunction_index < terminal_index:
                        terminal_index = conjunction_index
            name = name.replace(name[conditional_index:terminal_index], '')

    return name


def split_exclusive_conjunctions(words, conjunction):
    conjunction = conjunction.strip()
    left = sanitize_name([' '.join(words[:words.index(conjunction)])]).split()
    right = sanitize_name([' '.join(words[words.index(conjunction) + 1:])]).split()
    if len(left) > len(right):
        return [' '.join(left)]
    elif len(right) > len(left):
        return [' '.join(right)]

    return [' '.join(left), ' '.join(right)]


def split_additive_conjunctions(ingredient, words, conjunction):
    conjunction = conjunction.strip()
    left_name = ' '.join(words[:words.index(conjunction)])
    right_name = ' '.join(words[words.index(conjunction) + 1:])
    if ',' in left_name:
        _, primary_noun_index = get_closest_to_character(',', left_name, False, lambda char: char.isspace())
        right_name = left_name[primary_noun_index:left_name.index(',')] + ' ' + right_name
    elif ', ' in right_name:
        _, primary_noun_index = get_closest_to_character(', ', right_name, True, lambda char: char.isspace())
        left_name += ' ' + right_name[right_name.index(', ') + 2:primary_noun_index + 1]

    right_amount = 0
    if any(char.isdigit() for char in right_name):
        right_amount = Fraction(get_number_from_string(remove_irrelevant_phrases(right_name)))

    left_name = sanitize_name([left_name])
    right_name = sanitize_name([right_name])

    if left_name and right_name in IGNORED_CONJUNCTION_INGREDIENTS:
        ingredient['name'] = sanitize_name([ingredient['name']])
        return
    if left_name in IRRELEVANT_INGREDIENTS:
        ingredient['name'] = right_name
        return
    if right_name in IRRELEVANT_INGREDIENTS:
        ingredient['name'] = left_name
        return
    if left_name == right_name:
        ingredient['name'] = left_name
        if right_amount:
            ingredient['amount'] = str(Fraction(ingredient['amount']) + right_amount)
        return

    amount = ingredient['amount']
    if not right_amount:
        amount = right_amount = str(Fraction(ingredient['amount']) / 2)
    ingredient['amount'] = amount
    ingredient['name'] = left_name

    return {
        'amount': str(right_amount),
        'name': right_name,
        'unit': ingredient['unit']
    }


def is_conjunction_between_amount(conjunction, string):
    words = split_words_on_conjunction(conjunction, string)
    conjunction_index = words.index(conjunction.strip())

    return (words[conjunction_index - 1].isdigit()
            or words[conjunction_index + conjunction_index < len(words) - 1].isdigit())


def split_words_on_conjunction(contextual_conjunction, string):
    return string.replace(contextual_conjunction, ' ' + contextual_conjunction + ' ').split()


def get_contextual_conjunction(conjunction, name):
    if len(conjunction) == 1:
        return conjunction

    contextual_conjunction = ' ' + conjunction + ','
    if contextual_conjunction in name:
        return contextual_conjunction

    return ' ' + conjunction + ' '
