from copy import deepcopy
from difflib import SequenceMatcher

from constants.grocery_list import (IRRELEVANT_WORDS, INGREDIENT_COMMON_ADJECTIVES, PREFERRED_NAME_OVERRIDES,
                                    ALL_DERIVED_UNITS)


def sanitize_name(names):
    return get_preferred_name(map(remove_irrelevant_words, [name.lower() for name in names]))


def remove_irrelevant_words(name):
    name = filter(lambda char: not char.isdigit(), name)
    irrelevant_words_in_name = filter(lambda word: is_word_irrelevant_in_context(word, name),
                                      IRRELEVANT_WORDS + ALL_DERIVED_UNITS)
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

    return name.strip()


def is_word_irrelevant_in_context(word, name):
    if word not in name:
        return False

    preceding_char = name[name.index(word) - 1] if name.index(word) > 0 else ' '
    succeeding_char = name[name.index(word) + len(word)] if (name.index(word) + len(word)) < len(name) else ' '

    if word in ALL_DERIVED_UNITS and len(word) == 1:
        return is_adjacent_char_irrelevant(preceding_char) and is_adjacent_char_irrelevant(succeeding_char)

    return is_adjacent_char_irrelevant(preceding_char) or is_adjacent_char_irrelevant(succeeding_char)


def is_adjacent_char_irrelevant(char):
    return char.isspace() or char in IRRELEVANT_WORDS


def get_preferred_name(names):
    derived_to_preferred_names = deepcopy(PREFERRED_NAME_OVERRIDES)
    for preferred_name, derived_names in INGREDIENT_COMMON_ADJECTIVES.items():
        preferred_name_override = PREFERRED_NAME_OVERRIDES.get(preferred_name) or preferred_name
        derived_to_preferred_names[preferred_name] = preferred_name_override
        for derived_name in derived_names:
            derived_to_preferred_names[preferred_name + ' ' + derived_name] = preferred_name_override

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

