from constants.grocery_list import ADDITIVE_CONJUNCTIONS, EXCLUSIVE_CONJUNCTIONS, VALID_UNITS
from helpers.grocery_list.name_sanitization import sanitize_name, get_preferred_name


def split_conjunctions(ingredient):
    ingredients = [ingredient]
    for conjunction in ADDITIVE_CONJUNCTIONS + EXCLUSIVE_CONJUNCTIONS:
        if conjunction in ingredient['name'] and not is_conjunction_between_numbers(conjunction, ingredient['name']):
            words, word_with_conjunction = split_words_on_conjunction(conjunction, ingredient['name'])
            if conjunction in ADDITIVE_CONJUNCTIONS:
                halved_amount = ingredient['amount'] / 2
                ingredient['amount'] = halved_amount
                ingredient['name'] = sanitize_name(''.join(words[:words.index(word_with_conjunction)]))

                ingredients.append({
                    'amount': halved_amount,
                    'name': sanitize_name(''.join(words[words.index(word_with_conjunction) + 1:])),
                    'unit': ingredient['unit']
                })
            else:
                if is_conjunction_between_amount(conjunction, ingredient['name']):
                    for word in words:
                        if word.isdigit() or word in VALID_UNITS or word == word_with_conjunction:
                            ingredient['name'] = ingredient['name'].replace(word, '')
                    ingredient['name'] = ' '.join(ingredient['name'].split())
                else:
                    ingredient['name'] = get_preferred_name(split_exclusive_conjunctions(
                        ingredient['name'], words, word_with_conjunction))
    ingredient['name'] = get_preferred_name([sanitize_name(ingredient['name'])])
    return ingredients


def split_exclusive_conjunctions(name, words, word_with_conjunction):
    names = []

    left = words[:words.index(word_with_conjunction)]
    right = words[words.index(word_with_conjunction) + 1:]
    if len(left) > len(right):
        names.append(sanitize_name(' '.join(left)))
    elif len(right) > len(left):
        names.append(sanitize_name(' '.join(right)))
    else:
        names += [sanitize_name(' '.join(left)), sanitize_name(' '.join(right))]

    return names or [name]


def is_conjunction_between_numbers(conjunction, string):
    words, word_with_conjunction = split_words_on_conjunction(conjunction, string)
    return (words[words.index(word_with_conjunction) - 1].isdigit()
            and words[words.index(word_with_conjunction) + 1].isdigit())


def is_conjunction_between_amount(conjunction, string):
    words, word_with_conjunction = split_words_on_conjunction(conjunction, string)
    word_with_conjunction_index = words.index(word_with_conjunction)

    return (words[word_with_conjunction_index - 1].isdigit()
            or words[word_with_conjunction_index + word_with_conjunction_index < len(words) - 1].isdigit())


def split_words_on_conjunction(conjunction, string):
    words = string.split(' ')
    word_with_conjunction = [word for word in words if conjunction in word][0]

    return words, word_with_conjunction
