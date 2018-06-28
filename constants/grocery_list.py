from fractions import Fraction

ADDITIVE_CONJUNCTIONS = ['and', '&']
EXCLUSIVE_CONJUNCTIONS = ['or', '/']
CONDITIONAL_CONJUNCTIONS = ['if']
IGNORED_CONJUNCTION_INGREDIENTS = ['half']

INGREDIENT_COMMON_ADJECTIVES = {
    'pepper': ['black', 'cracked'],
    'chili flake': ['red'],
    'flour': ['all purpose'],
    'salt': ['kosher'],
    'oil': ['olive', 'cooking'],
    'parmesan cheese': ['grated'],
    'onion': ['yellow'],
    'broth': ['vegetable'],
    'paprika': ['smoked', 'ground'],
    'cumin': ['ground', 'powder'],
    'egg': ['yolk', 'white'],
    'sugar': ['granulated', 'white'],
    'confectioners sugar': ['powdered'],
    'butter': ['unsalted'],
    'heavy cream': ['whipping'],
    'coconut milk': ['full fat'],
    'cilantro': ['leaves'],
    'cinnamon': ['ground'],
    'chickpeas': ['canned'],
    'lentils': ['red'],
    'maple': ['syrup'],
    'jalapeno': ['pepper'],
    'coconut oil': ['virigin'],
    'olive oil': ['virigin']
}

INGREDIENT_SYNONYMS = {
    'coriander': 'cilantro',
    'confectioners sugar': 'powdered sugar',
    'coriander ground': 'coriander powder'
}

PREFERRED_NAME_OVERRIDES = {
    'broth': 'vegetable broth',
    'oil': 'olive oil',
    'onion': 'yellow onion',
    'potato': 'russet potato',
    'cheese': 'cheddar cheese',
    'shredded cheese': 'shredded cheddar cheese',
    'maple': 'maple syrup'
}

IRRELEVANT_WORDS = [
    'fresh',
    'freshly',
    'small',
    'large',
    'medium',
    'see notes',
    'optional',
    'peeled',
    'cut',
    'into pieces',
    'with stems removed',
    'super',
    'firm',
    'cooked',
    '*',
    '(',
    ')',
    '+',
    ',',
    'vegan',
    'reduced',
    '-',
    'to drizzle',
    '%',
    'pure',
    'of',
    'smooth',
    'block',
    '.',
    'chopped',
    'roasted',
    'extra',
    'other',
    'creamy',
    'drippy',
    'packed',
    'roasted',
    'thai',
    '/',
    'flaky',
    'head',
    'thawed',
    'defrost',
    'minced',
    'hard',
    'soft',
    'boil in bag'
]

IRRELEVANT_INGREDIENTS = [
    'n/a',
    'water',
    'ice water',
    'topping',
    ''
]

IRRELEVANT_PHRASES = [
    'for the'
]

UNITS = {
    'oz': {
        'synonyms': ['ounce'],
        'conversion': {}
    },
    'lb': {
        'synonyms': [],
        'conversion': {}
    },
    'tsp': {
        'synonyms': ['teaspoon'],
        'conversion': {}
    },
    'cup': {
        'synonyms': ['c'],
        'conversion': {'unit': 'tbsp', 'ratio': 16}
    },
    'dash': {
        'synonyms': [],
        'conversion': {'unit': 'tsp', 'ratio': Fraction(1, 8)}
    },
    'jar': {
        'synonyms': [],
        'conversion': {}
    },
    'tbsp': {
        'synonyms': ['tablespoon'],
        'conversion': {'unit': 'tsp', 'ratio': 3}
    },
    'ml': {
        'synonyms': [],
        'conversion': {}
    },
    'g': {
        'synonyms': [],
        'conversion': {}
    },
    'can': {
        'synonyms': [],
        'conversion': {'unit': 'oz', 'ratio': 14}
    },
    'clove': {
        'synonyms': [],
        'conversion': {}
    },
    'sheet': {
        'synonyms': [],
        'conversion': {}
    },
    'leaves': {
        'synonyms': [],
        'conversion': {}
    }
}

ALL_DERIVED_UNITS = []
for unit, unit_properties in UNITS.items():
    ALL_DERIVED_UNITS += [unit] + unit_properties['synonyms']

IGNORED_MINOR_TO_MAJOR = ['dash', 'can']

MINOR_TO_MAJOR_CONVERSIONS = {}
for unit, unit_properties in UNITS.items():
    if unit_properties['conversion'] and unit not in IGNORED_MINOR_TO_MAJOR:
        MINOR_TO_MAJOR_CONVERSIONS[unit_properties['conversion']['unit']] = {
            'conversion': {
                'unit': unit,
                'ratio': Fraction(1, unit_properties['conversion']['ratio'])
            }
        }

MAJOR_VOLUME_WEIGHT_CONVERSIONS = {
    'butter': {
        'tsp': {
            'conversion': {'unit': 'g', 'ratio': Fraction(19, 4)}
        },
    },
    'flour': {
        'tsp': {
            'conversion': {'unit': 'g', 'ratio': Fraction(10, 3)}
        },
    },
    'coconut milk': {
        'oz': {
            'conversion': {'unit': 'cup', 'ratio': Fraction(1, 8)}
        },
    },
    'kale': {
        'leaves': {
            'conversion': {'unit': 'cup', 'ratio': 1}
        }
    },
    'cilantro': {
        'cup': {
            'conversion': {'unit': 'leaves', 'ratio': 1}
        },
    },
    'basil': {
        'cup': {
            'conversion': {'unit': '', 'ratio': 1}
        }
    },
    'carrots': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': Fraction(1, 3)}
        }
    },
    'yellow onion': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': 1}
        }
    },
    'garlic': {
        'clove': {
            'conversion': {'unit': 'tsp', 'ratio': 1}
        }
    },
    'lemon juice': {
        'tbsp': {
            'conversion': {'unit': '', 'ratio': Fraction(1, 2)}
        }
    },
    'lemon zest': {
        'tsp': {
            'conversion': {'unit': '', 'ratio': Fraction(1, 3)}
        }
    }
}

MINOR_VOLUME_WEIGHT_CONVERSIONS = {}
for ingredient, conversions in MAJOR_VOLUME_WEIGHT_CONVERSIONS.items():
    MINOR_VOLUME_WEIGHT_CONVERSIONS[ingredient] = {}
    for unit, unit_properties in conversions.items():
        MINOR_VOLUME_WEIGHT_CONVERSIONS[ingredient][unit_properties['conversion']['unit']] = {
            'conversion': {
                'unit': unit,
                'ratio': Fraction(1, unit_properties['conversion']['ratio'])
            }
        }
