from constants.grocery_list import ADDITIVE_CONJUNCTIONS, EXCLUSIVE_CONJUNCTIONS, UNITS
from helpers.grocery_list.name_sanitization import sanitize_name


def split_conjunctions(ingredient):
    ingredients = [ingredient]
    for conjunction in ADDITIVE_CONJUNCTIONS + EXCLUSIVE_CONJUNCTIONS:
        if (' ' + conjunction + ' ' in ingredient['name'] and
                not is_conjunction_between_numbers(conjunction, ingredient['name'])):
            words, word_with_conjunction = split_words_on_conjunction(conjunction, ingredient['name'])
            if conjunction in ADDITIVE_CONJUNCTIONS:
                halved_amount = ingredient['amount'] / 2
                ingredient['amount'] = halved_amount
                ingredient['name'] = sanitize_name([' '.join(words[:words.index(word_with_conjunction)])])

                ingredients.append({
                    'amount': halved_amount,
                    'name': sanitize_name([' '.join(words[words.index(word_with_conjunction) + 1:])]),
                    'unit': ingredient['unit']
                })
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


def is_conjunction_between_numbers(conjunction, string):
    left = get_closest_non_space_to_conjunction(conjunction, string, False)
    right = get_closest_non_space_to_conjunction(conjunction, string, True)
    return left.isdigit() and right.isdigit()


def get_closest_non_space_to_conjunction(conjunction, string, incrementing):
    closest = ''
    closest_index = string.index(conjunction) + (1 if incrementing else -1)
    while (not closest and not closest.isspace() and
           (closest_index < len(string) if incrementing else closest_index >= 0)):
        closest = string[closest_index]
        closest_index += 1 if incrementing else -1

    return closest


def is_conjunction_between_amount(conjunction, string):
    words, word_with_conjunction = split_words_on_conjunction(conjunction, string)
    word_with_conjunction_index = words.index(word_with_conjunction)

    return (words[word_with_conjunction_index - 1].isdigit()
            or words[word_with_conjunction_index + word_with_conjunction_index < len(words) - 1].isdigit())


def split_words_on_conjunction(conjunction, string):
    words = string.split(' ')
    word_with_conjunction = [word for word in words if conjunction in word][0]

    return words, word_with_conjunction
