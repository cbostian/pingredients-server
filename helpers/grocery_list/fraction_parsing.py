import unicodedata
from fractions import Fraction

from helpers.grocery_list.conjunction_parsing import is_conjunction_between_numbers

VF = 'VULGAR FRACTION '
VULGAR_FRACTIONS = {
    unicodedata.lookup(VF + 'ONE EIGHTH'): Fraction(1, 8),
    unicodedata.lookup(VF + 'ONE FIFTH'): Fraction(1, 5),
    unicodedata.lookup(VF + 'ONE QUARTER'): Fraction(1, 4),
    unicodedata.lookup(VF + 'THREE EIGHTHS'): Fraction(3, 8),
    unicodedata.lookup(VF + 'TWO FIFTHS'): Fraction(2, 5),
    unicodedata.lookup(VF + 'ONE HALF'): Fraction(1, 2),
    unicodedata.lookup(VF + 'THREE FIFTHS'): Fraction(3, 5),
    unicodedata.lookup(VF + 'FIVE EIGHTHS'): Fraction(5, 8),
    unicodedata.lookup(VF + 'THREE QUARTERS'): Fraction(3, 4),
    unicodedata.lookup(VF + 'FOUR FIFTHS'): Fraction(4, 5),
    unicodedata.lookup(VF + 'SEVEN EIGHTHS'): Fraction(7, 8),
    unicodedata.lookup(VF + 'ONE THIRD'): Fraction(1, 3),
    unicodedata.lookup(VF + 'TWO THIRDS'): Fraction(2, 3),
    unicodedata.lookup(VF + 'ONE SIXTH'): Fraction(1, 6),
    unicodedata.lookup(VF + 'FIVE SIXTHS'): Fraction(5, 6),
}


def convert_unicode_fractions(string_to_convert):
    unicode_string = string_to_convert.decode('unicode-escape')
    unicode_fraction = filter(lambda x: unicodedata.name(x).startswith(VF), unicode_string)
    if unicode_fraction:
        string_to_convert = unicode_string.replace(unicode_fraction, str(VULGAR_FRACTIONS[unicode_fraction]))
    return str(string_to_convert)


def is_character_part_of_fraction(character, string):
    return (character.isdigit() or (character == '/' and is_conjunction_between_numbers('/', string))
            or character.isspace())


def convert_fractions(string_to_convert):
    fraction = ''.join(filter(lambda x: is_character_part_of_fraction(x, string_to_convert), string_to_convert)).strip()
    if not fraction or '/' not in string_to_convert:
        return string_to_convert
    transformed_fraction = str(sum(Fraction(num) for num in fraction.split()))
    return convert_unicode_fractions(string_to_convert.replace(fraction, transformed_fraction))
