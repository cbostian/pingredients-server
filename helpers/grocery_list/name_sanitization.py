from difflib import SequenceMatcher

from constants.grocery_list import (IRRELEVANT_WORDS, INGREDIENT_COMMON_ADJECTIVES, PREFERRED_NAME_OVERRIDES,
                                    ALL_DERIVED_UNITS)


def sanitize_name(names):
    return get_preferred_name(map(remove_irrelevant_words, [name.lower() for name in names]))


def remove_irrelevant_words(name):
    irrelevant_words_in_name = filter(lambda word: word in name, IRRELEVANT_WORDS +
                                      [' ' + unit + ('' if len(unit) > 1 else ' ') for unit in ALL_DERIVED_UNITS])
    while any(word in name for word in irrelevant_words_in_name) and irrelevant_words_in_name:
        irrelevant_word = irrelevant_words_in_name.pop(0)

        try:
            irrelevant_word_index = name.index(irrelevant_word)
        except ValueError:
            continue

        to_remove = irrelevant_word
        next_space_index = name.find(' ', irrelevant_word_index)
        if next_space_index > 0 and len(irrelevant_word) > 1 and ' ' not in irrelevant_word:
            to_remove = name[irrelevant_word_index:next_space_index]

        name = name.replace(to_remove, ' ')

    name = filter(lambda char: not char.isdigit(), name)
    return name.strip()


def get_preferred_name(names):
    derived_to_preferred_names = {}
    for preferred_name, derived_names in INGREDIENT_COMMON_ADJECTIVES.items():
        derived_to_preferred_names[preferred_name] = preferred_name = (PREFERRED_NAME_OVERRIDES.get(preferred_name)
                                                                       or preferred_name)
        for derived_name in derived_names:
            derived_to_preferred_names[preferred_name + ' ' + derived_name] = preferred_name

    best_name = names[0]
    max_match = 0.7857142857142856

    for name in names:
        for derived_name, preferred_name in derived_to_preferred_names.items():
            match = SequenceMatcher(None, ''.join(sorted(name.lower().split(' '))),
                                    ''.join(sorted(derived_name.lower().split(' ')))).ratio()
            if match > max_match:
                best_name = preferred_name
                max_match = match
    return best_name

