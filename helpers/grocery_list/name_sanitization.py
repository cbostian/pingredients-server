import re
from copy import deepcopy
from difflib import SequenceMatcher

from constants.grocery_list import (IRRELEVANT_PHRASES, IRRELEVANT_WORDS, INGREDIENT_COMMON_ADJECTIVES,
                                    INGREDIENT_SYNONYMS, PREFERRED_NAME_OVERRIDES, ALL_DERIVED_UNITS)


def sanitize_name(names):
    return ' '.join(get_preferred_name(map(remove_irrelevant_words, [name.lower() for name in names])).split())


def remove_irrelevant_words(name):
    name = remove_irrelevant_phrases(name)
    name = filter(lambda char: not (char.isdigit() or char in IRRELEVANT_WORDS), name)
    irrelevant_words = get_all_irrelevant_words(name)
    while any(word in name for word in irrelevant_words) and irrelevant_words:
        irrelevant_word = irrelevant_words.pop(0)
        try:
            irrelevant_word_index = name.index(irrelevant_word)
        except ValueError:
            continue

        next_terminal_index = next_space_index = name.find(' ', irrelevant_word_index + len(irrelevant_word))
        if next_space_index < 0:
            next_terminal_index = len(name) - 1
        name = name.replace(name[irrelevant_word_index:next_terminal_index + 1], ' ')

    unique_words = set()
    return ' '.join([w for w in name.split() if not (w in unique_words or unique_words.add(w))])


def get_all_irrelevant_words(name):
    irrelevant_words_in_context = []
    irrelevant_words = filter(lambda irrelevant_word: len(irrelevant_word) > 1, IRRELEVANT_WORDS) + ALL_DERIVED_UNITS
    for phrase in irrelevant_words:
        words = phrase.split()
        if not is_phrase_in_word(words, name):
            continue
        to_remove = name[name.index(words[0]):name.index(words[len(words) - 1]) + len(words[len(words) - 1])]
        occurrences = [match.start() for match in re.finditer(re.escape(to_remove), name)]
        for index in occurrences:
            preceding_char, succeeding_char = get_adjacent_characters(index, to_remove, name)
            if is_word_irrelevant_in_context(to_remove, preceding_char, succeeding_char):
                irrelevant_words_in_context.append((preceding_char + to_remove + succeeding_char).strip())

    return irrelevant_words_in_context


def get_adjacent_characters(index, word, string_with_word):
    preceding_char = string_with_word[index - 1] if index > 0 else ''
    succeeding_char = string_with_word[index + len(word)] if (index + len(word)) < len(string_with_word) else ''
    return preceding_char, succeeding_char


def is_phrase_in_word(phrase, name):
    for word in phrase:
        if word not in name:
            return False

    return True


def is_word_irrelevant_in_context(word, preceding_char, succeeding_char):
    if word in ALL_DERIVED_UNITS:
        return is_adjacent_char_irrelevant(preceding_char) and (is_adjacent_char_irrelevant(succeeding_char)
                                                                or succeeding_char == 's')

    return is_adjacent_char_irrelevant(preceding_char) and is_adjacent_char_irrelevant(succeeding_char)


def is_adjacent_char_irrelevant(char):
    return char.isspace() or char in IRRELEVANT_WORDS or not char


def remove_irrelevant_phrases(name):
    for phrase in IRRELEVANT_PHRASES:
        if phrase in name:
            name = name[:name.index(phrase)]

    return name


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
    return INGREDIENT_SYNONYMS.get(best_name, best_name)

