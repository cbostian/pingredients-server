from constants.grocery_list import ADDITIVE_CONJUNCTIONS, EXCLUSIVE_CONJUNCTIONS, UNITS
from helpers.grocery_list.name_sanitization import sanitize_name


def split_conjunctions(ingredient):
    ingredients = [ingredient]
    for conjunction in ADDITIVE_CONJUNCTIONS + EXCLUSIVE_CONJUNCTIONS:
        if (' ' + conjunction + ' ' in ingredient['name'] and
                not is_conjunction_between_numbers(conjunction, ingredient['name'])):
            words, word_with_conjunction = split_words_on_conjunction(conjunction, ingredient['name'])
            if conjunction in ADDITIVE_CONJUNCTIONS:
                ingredients.append(split_additive_conjunctions(ingredient, words, word_with_conjunction))
            else:
                if is_conjunction_between_amount(conjunction, ingredient['name']):
                    for word in words:
                        if word.isdigit() or word in UNITS.keys() or word == word_with_conjunction:
                            ingredient['name'] = ingredient['name'].replace(word, '')
                else:
                    ingredient['name'] = sanitize_name(split_exclusive_conjunctions(
                        ingredient['name'], words, word_with_conjunction))
    ingredient['name'] = sanitize_name([ingredient['name']])
    return ingredients


def split_exclusive_conjunctions(name, words, word_with_conjunction):
    names = []

    left = words[:words.index(word_with_conjunction)]
    right = words[words.index(word_with_conjunction) + 1:]
    if len(left) > len(right):
        names.append(' '.join(left))
    elif len(right) > len(left):
        names.append(' '.join(right))
    else:
        names += [' '.join(left), ' '.join(right)]

    return names or [name]


def split_additive_conjunctions(ingredient, words, word_with_conjunction):
    left_name = ' '.join(words[:words.index(word_with_conjunction)])
    right_name = ' '.join(words[words.index(word_with_conjunction) + 1:])
    if ',' in left_name:
        _, primary_noun_index = get_closest_to_character(',', left_name, False, lambda char: char.isspace())
        right_name = left_name[primary_noun_index:left_name.index(',')] + ' ' + right_name
    elif ',' in right_name:
        _, primary_noun_index = get_closest_to_character(', ', right_name, True, lambda char: char.isspace())
        left_name += ' ' + right_name[right_name.index(', ') + 2:primary_noun_index + 1]

    halved_amount = ingredient['amount'] / 2
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
    words, word_with_conjunction = split_words_on_conjunction(conjunction, string)
    word_with_conjunction_index = words.index(word_with_conjunction)

    return (words[word_with_conjunction_index - 1].isdigit()
            or words[word_with_conjunction_index + word_with_conjunction_index < len(words) - 1].isdigit())


def split_words_on_conjunction(conjunction, string):
    words = string.split(' ')
    word_with_conjunction = [word for word in words if conjunction in word][0]

    return words, word_with_conjunction
