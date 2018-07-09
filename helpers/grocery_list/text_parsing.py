def is_word_between_numbers(word, string):
    left, _ = get_closest_to_character(word, string, False)
    right, _ = get_closest_to_character(word, string, True)
    return left.isdigit() and right.isdigit()


def get_closest_to_character(character, string, incrementing, condition=lambda char: not char.isspace()):
    closest_index = (string.index(character) + (1 if incrementing else -1) +
                     (len(character) if len(character) > 1 and incrementing else 0))
    if closest_index < 0 or closest_index > (len(string) - 1):
        return '', string.index(character)
    closest = string[closest_index]
    while not condition(closest) and (closest_index < (len(string) - 1) if incrementing else closest_index > 0):
        closest_index += 1 if incrementing else -1
        closest = string[closest_index]

    return closest, closest_index


def get_pluralizations(name):
    names = [name]
    plural_endings = ['s', 'es', 'ed']

    for plural_ending in plural_endings:
        names.append(name + plural_ending)

    return names
