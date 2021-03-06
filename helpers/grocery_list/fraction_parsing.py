import unicodedata
from fractions import Fraction

from helpers.grocery_list.text_parsing import is_word_between_numbers

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

DISPLAY_FRACTIONS = []
for denominator in range(7):
    for numerator in range(denominator + 2):
        display_fraction = Fraction(numerator + 1, denominator + 2)
        if (numerator + 1) < (denominator + 2) and display_fraction not in DISPLAY_FRACTIONS:
            DISPLAY_FRACTIONS.append(Fraction(numerator + 1, denominator + 2))


def convert_unicode_fractions(string_to_convert):
    unicode_fraction = filter(lambda x: unicodedata.name(x).startswith(VF), string_to_convert)
    if unicode_fraction:
        string_to_convert = string_to_convert.replace(unicode_fraction, str(VULGAR_FRACTIONS[unicode_fraction]))
    return str(string_to_convert)


def is_character_part_of_fraction(character, string):
    return (character.isdigit() or (character == '/' and is_word_between_numbers('/', string))
            or character.isspace())


def convert_fractions(string_to_convert):
    string_to_convert = string_to_convert.encode('ascii', 'ignore').decode('unicode-escape')
    fractions = []
    temp_fraction = ''
    for char in string_to_convert:
        if is_character_part_of_fraction(char, string_to_convert):
            temp_fraction += char
        elif temp_fraction.strip():
            if '/' in temp_fraction:
                fractions.append(temp_fraction)
            temp_fraction = ''

    for fraction in fractions:
        string_to_convert = string_to_convert.replace(fraction, ' ' +
                                                      str(sum(Fraction(num.strip()) for num in fraction.split())) + ' ')

    return convert_unicode_fractions(string_to_convert)


def set_display_amount(ingredient):
    amount = Fraction(ingredient['amount'])
    if amount.denominator < 9:
        ingredient['display_amount'] = ingredient['amount']
        return

    remainder = Fraction(amount.numerator % amount.denominator, amount.denominator)
    closest_display_fraction = 1
    for fraction in DISPLAY_FRACTIONS:
        if abs(remainder - fraction) < abs(remainder - closest_display_fraction):
            closest_display_fraction = fraction

    ingredient['display_amount'] = str(amount - remainder + closest_display_fraction)

