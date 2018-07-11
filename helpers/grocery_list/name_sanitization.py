import re
from difflib import SequenceMatcher

from constants.grocery_list import (ALL_DERIVED_UNITS, DERIVED_TO_PREFERRED_NAMES, HOMONYM_UNITS,
                                    IGNORED_CONJUNCTION_INGREDIENTS, IRRELEVANT_PHRASES, IRRELEVANT_WORDS,
                                    INGREDIENT_SYNONYMS, MIN_SIMILARITY_TO_COMBINE, PARTIAL_SYNONYMS)

irrelevant_words_time = preferred_name_time = 0


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

        next_terminal_index = next_space_index = name.find(' ', irrelevant_word_index + len(irrelevant_word))
        if next_space_index < 0:
            next_terminal_index = len(name) - 1
        name = name.replace(name[irrelevant_word_index:next_terminal_index + 1], ' ')

    unique_words = set()
    return ' '.join([w for w in name.split() if not (w in unique_words or unique_words.add(w))
                     or w in IGNORED_CONJUNCTION_INGREDIENTS])


def get_all_irrelevant_words(name):
    irrelevant_words_in_context = []
    irrelevant_words = (filter(lambda irrelevant_word: len(irrelevant_word) > 1, IRRELEVANT_WORDS) +
                        [unit for unit in ALL_DERIVED_UNITS if unit not in HOMONYM_UNITS])
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
    return char.isspace() or char in IRRELEVANT_WORDS or not char or char.isdigit()


def remove_irrelevant_phrases(name):
    if '(' in name and ')' in name:
        name = name.replace(name[name.index('('):name.index(')') + 1], ' ')
    for phrase in IRRELEVANT_PHRASES:
        if phrase in name:
            name = name[:name.index(phrase)]

    return name


def get_preferred_name(names):
    best_name = names[0]
    max_match = MIN_SIMILARITY_TO_COMBINE

    for name in names:
        for derived_name, preferred_name in DERIVED_TO_PREFERRED_NAMES.items():
            if name == derived_name:
                return preferred_name
            match = get_name_similarity(name, derived_name)
            if match > max_match:
                best_name = preferred_name
                max_match = match

    if best_name == names[0]:
        for synonym, original in PARTIAL_SYNONYMS.items():
            best_name = best_name.replace(synonym, original)

    return INGREDIENT_SYNONYMS.get(best_name, best_name)


def get_name_similarity(name1, name2):
    return SequenceMatcher(None, ''.join(sorted(name1.lower().split())), ''.join(sorted(name2.lower().split()))).ratio()
