from helpers.grocery_list.fraction_parsing import convert_fractions, is_character_part_of_fraction
from helpers.grocery_list.text_parsing import get_closest_to_character


def prepare_for_amount_parsing(string):
    string = convert_fractions(string)
    string = handle_ranges(string)
    string = handle_dimensions(string)
    return string


def handle_ranges(string):
    string = string.replace('-', ' - ')
    words = string.split()
    try:
        range_index = words.index('-')
        left = words[range_index - 1 if range_index > 0 else 0]
        right = words[range_index + 1 if range_index < len(words) - 1 else 0]
        if filter(lambda char: char.isdigit(), left) and filter(lambda char: char.isdigit(), right):
            string = string.replace(left, '')
            string = string.replace('-', '')
        return string
    except ValueError:
        return string


def handle_dimensions(string):
    dimension_char = 'x'
    if dimension_char not in string:
        return string
    left, left_index = get_closest_to_character(dimension_char, string, False)
    right, right_index = get_closest_to_character(dimension_char, string, True)

    if not(left.isdigit() and right.isdigit()):
        return string

    while is_number_part_of_other_number(left_index, left, string) and left_index > 0:
        left_index -= 1
        if not(string[left_index].isdigit() or string[left_index] == '/'):
            break
        left = string[left_index]

    while is_number_part_of_other_number(right_index, right, string) and right_index < (len(string) - 1):
        right_index += 1
        if not(string[right_index].isdigit() or string[right_index] == '/'):
            break
        right = string[right_index]

    return string.replace(string[left_index:right_index + 1], ' ')


def is_number_part_of_other_number(number_index, number, string):
    is_preceding_part_of_number = False
    is_succeeding_part_of_number = False

    if number_index > 0:
        is_preceding_part_of_number = string[number_index - 1].isdigit() or string[number_index - 1] == '/'

    if number_index + len(number) < len(string):
        is_succeeding_part_of_number = string[number_index + len(number)].isdigit() or (
                string[number_index + len(number)] == '/' and (number_index + len(number)) < (len(string) - 1))

    return is_preceding_part_of_number or is_succeeding_part_of_number


def get_number_from_string(string):
    all_numbers = ''.join(filter(lambda x: is_character_part_of_fraction(x, string), string)).split() or ['1']
    return all_numbers[1] if all_numbers[0] == '1' and len(all_numbers) > 1 else all_numbers[0]
