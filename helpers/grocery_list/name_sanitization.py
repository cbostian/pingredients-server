from difflib import SequenceMatcher

from constants.grocery_list import IRRELEVANT_WORDS
from constants.grocery_list import INGREDIENT_COMMON_ADJECTIVES, PREFERRED_NAME_OVERRIDES


def sanitize_name(name):
    sanitized_name = name.lower()
    sanitized_name = remove_irrelevant_words(sanitized_name)

    return sanitized_name.strip()


def remove_irrelevant_words(string):
    irrelevant_words_in_string = filter(lambda word: word in string, IRRELEVANT_WORDS)
    while any(word in string or word.isdigit() for word in irrelevant_words_in_string) and irrelevant_words_in_string:
        string = string.replace(irrelevant_words_in_string.pop(0), '')

    string = filter(lambda char: not char.isdigit(), string)
    return string


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

