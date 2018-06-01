from constants.grocery_list import IRRELEVANT_WORDS


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
