import re
from copy import deepcopy
from difflib import SequenceMatcher

from constants.grocery_list import (IRRELEVANT_WORDS, INGREDIENT_COMMON_ADJECTIVES, PREFERRED_NAME_OVERRIDES,
                                    ALL_DERIVED_UNITS)


def sanitize_name(names):
    return ' '.join(get_preferred_name(map(remove_irrelevant_words, [name.lower() for name in names])).split())


def remove_irrelevant_words(name):
    name = filter(lambda char: not (char.isdigit() or char in IRRELEVANT_WORDS), name)
    irrelevant_words = get_all_irrelevant_words(name)
    while any(word in name for word in irrelevant_words) and irrelevant_words:
        irrelevant_word = irrelevant_words.pop(0)
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


def get_all_irrelevant_words(name):
    irrelevant_words_in_context = []
    irrelevant_words = filter(lambda irrelevant_word: len(irrelevant_word) > 1, IRRELEVANT_WORDS) + ALL_DERIVED_UNITS
    for word in irrelevant_words:
        if word not in name:
            continue
        word_occurrences = [match.start() for match in re.finditer(re.escape(word), name)]
        for index in word_occurrences:
            preceding_char = name[index - 1] if index > 0 else ''
            succeeding_char = name[index + len(word)] if (index + len(word)) < len(name) else ''
            if is_word_irrelevant_in_context(word, preceding_char, succeeding_char):
                irrelevant_words_in_context.append(preceding_char + word + succeeding_char)

    return irrelevant_words_in_context


def is_word_irrelevant_in_context(word, preceding_char, succeeding_char):
    if word in ALL_DERIVED_UNITS and len(word) == 1:
        return is_adjacent_char_irrelevant(preceding_char) and is_adjacent_char_irrelevant(succeeding_char)

    return is_adjacent_char_irrelevant(preceding_char) or is_adjacent_char_irrelevant(succeeding_char)


def is_adjacent_char_irrelevant(char):
    return char.isspace() or char in IRRELEVANT_WORDS or not char


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
            match = SequenceMatcher(None, ''.join(sorted(name.lower().split())),
                                    ''.join(sorted(derived_name.lower().split()))).ratio()
            if match > max_match:
                best_name = preferred_name
                max_match = match
    return best_name

