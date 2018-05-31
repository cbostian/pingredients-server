IRRELEVANT_WORDS = [
    'fresh',
    'small',
    'large',
    'medium',
    'see notes',
    'optional',
    'peeled',
    'cut',
    'pieces',
    'into',
    'with',
    'stems',
    'removed',
    'super',
    'firm',
    'cooked'
]


def remove_irrelevant_words(string):
    irrelevant_words_in_string = filter(lambda word: word in string, IRRELEVANT_WORDS)
    while any(word in string for word in irrelevant_words_in_string) and irrelevant_words_in_string:
        string = string[:string.index(irrelevant_words_in_string.pop(0))]
    return string

