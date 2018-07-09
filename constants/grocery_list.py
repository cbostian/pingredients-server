from fractions import Fraction

ADDITIVE_CONJUNCTIONS = ['and', '&', '+', 'plus']
EXCLUSIVE_CONJUNCTIONS = ['or', '/']
CONDITIONAL_CONJUNCTIONS = ['if']
IGNORED_CONJUNCTION_INGREDIENTS = ['half']

MIN_SIMILARITY_TO_COMBINE = 0.7857142857142856

INGREDIENT_COMMON_ADJECTIVES = {
    'pepper': ['black', 'cracked'],
    'chili flake': ['red'],
    'flour': ['all purpose'],
    'salt': ['kosher', 'table'],
    'oil': ['olive', 'cooking'],
    'parmesan cheese': ['grated'],
    'onion': ['yellow'],
    'broth': ['vegetable'],
    'paprika': ['smoked', 'ground'],
    'turmeric': ['ground', 'powder'],
    'nutmeg': ['ground', 'powder'],
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
    'lentils': ['red', 'green', 'brown'],
    'maple': ['syrup'],
    'jalapeno': ['pepper'],
    'coconut oil': ['virigin'],
    'olive oil': ['virigin'],
    'peas frozen': ['green'],
    'brown sugar': ['dark'],
    'curry powder': ['yellow'],
    'curry paste': ['red'],
    'cocoa powder': ['black'],
    'vanilla': ['extract'],
    'mexican shredded cheese': ['style'],
    'sweet potato': ['purple'],
    'cacao powder': ['dutch', 'dutch process'],
    'wheat flour': ['white'],
    'ginger': ['root'],
    'dates': ['medjool'],
    'chili powder': ['red']
}

INGREDIENT_SYNONYMS = {
    'coriander': 'cilantro',
    'confectioners sugar': 'powdered sugar',
    'coriander ground': 'coriander powder',
    'chicken': 'chicken breast'
}

PARTIAL_SYNONYMS = {
    'stock': 'broth',
}

PREFERRED_NAME_OVERRIDES = {
    'broth': 'vegetable broth',
    'oil': 'olive oil',
    'onion': 'yellow onion',
    'potato': 'russet potato',
    'cheese': 'cheddar cheese',
    'shredded cheese': 'shredded cheddar cheese',
    'maple': 'maple syrup',
    'vanilla': 'vanilla extract'
}

IRRELEVANT_WORDS = [
    'fresh',
    'freshly',
    'small',
    'large',
    'medium',
    'see',
    'notes',
    'optional',
    'peeled',
    'cut',
    'into pieces',
    'with stems removed',
    'super',
    'firm',
    'cooked',
    '(',
    ')',
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
    'flaky',
    'head',
    'thawed',
    'defrost',
    'finely minced to',
    'hard',
    'soft',
    'boil in bag',
    'salted',
    'raw',
    'whole',
    'kernel',
    'refined',
    'curly',
    'stems',
    'organic',
    'light',
    'low',
    'sodium',
    'unsweetened',
    'boneless',
    'skinless',
    'filtered',
    'squeezed',
    'granulated',
    'good quality',
    'semi sweet',
    'refrigerated',
    'grass fed',
    '"',
    'regular',
    'ripe',
    'underripe',
    'slightly',
    'cooled',
    'de stemmed',
    'home made',
    'pitted',
    'inch'
]

IRRELEVANT_INGREDIENTS = [
    'n/a',
    'water',
    'ice water',
    'topping',
    '',
]

IRRELEVANT_PHRASES = [
    'for the',
    'such as',
    'to cook',
    '*',
    'cut into'
]

UNITS = {
    'oz': {
        'synonyms': ['ounce'],
        'conversion': {'unit': 'g', 'ratio': 28}
    },
    'lb': {
        'synonyms': [],
        'conversion': {'unit': 'oz', 'ratio': 16}
    },
    'tsp': {
        'synonyms': ['teaspoon'],
        'conversion': {}
    },
    'cup': {
        'synonyms': ['c'],
        'conversion': {'unit': 'tbsp', 'ratio': 16}
    },
    'pinch': {
        'synonyms': ['pinches'],
        'conversion': {'unit': 'tsp', 'ratio': Fraction(1, 16)}
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
        'conversion': {}
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
    },
    'piece': {
        'synonyms': [],
        'conversion': {}
    },
    'package': {
        'synonyms': [],
        'conversion': {}
    },
    'bunch': {
        'synonyms': [],
        'conversion': {}
    },
    'pint': {
        'synonyms': [],
        'conversion': {'unit': 'cup', 'ratio': 2}
    }
}

HOMONYM_UNITS = ['clove', 'piece', 'can']

ALL_DERIVED_UNITS = []
for unit, unit_properties in UNITS.items():
    ALL_DERIVED_UNITS += [unit] + unit_properties['synonyms']

IGNORED_MINOR_TO_MAJOR = ['dash', 'can', 'pinch', 'pint']

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
    'sugar': {
        'tsp': {
            'conversion': {'unit': 'g', 'ratio': 4}
        },
    },
    'coconut milk': {
        'oz': {
            'conversion': {'unit': 'cup', 'ratio': Fraction(1, 8)}
        },
        'can': {
            'conversion': {'unit': 'oz', 'ratio': 14}
        },
    },
    'chickpeas': {
        'can': {
            'conversion': {'unit': 'oz', 'ratio': 15}
        },
    },
    'kale': {
        'leaves': {
            'conversion': {'unit': 'cup', 'ratio': 1}
        }
    },
    'cilantro': {
        'bunch': {
            'conversion': {'unit': 'tbsp', 'ratio': 16}
        },
        '': {
            'conversion': {'unit': 'cup', 'ratio': 1}
        },
        'leaves': {
            'conversion': {'unit': 'cup', 'ratio': 1}
        }
    },
    'basil': {
        'cup': {
            'conversion': {'unit': '', 'ratio': 1}
        },
        '': {
            'conversion': {'unit': 'tbsp', 'ratio': 16}
        }
    },
    'carrots': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': Fraction(1, 3)}
        },
        'tbsp': {
            'conversion': {'unit': 'g', 'ratio': Fraction(39, 4)}
        }
    },
    'cauliflower': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': 4}
        },
        'tsp': {
            'conversion': {'unit': 'g', 'ratio': Fraction(29, 10)}
        }
    },
    'dates': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': Fraction(1, 8)}
        }
    },
    'avocado': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': Fraction(5, 4)}
        },
    },
    'russet potato': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': 1}
        },
        'tsp': {
            'conversion': {'unit': 'g', 'ratio': Fraction(77, 10)}
        }
    },
    'sweet potato': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': Fraction(2, 3)}
        },
        'tsp': {
            'conversion': {'unit': 'g', 'ratio': Fraction(18, 5)}
        }
    },
    'onion': {
        '': {
            'conversion': {'unit': 'cup', 'ratio': 1}
        },
        'tsp': {
            'conversion': {'unit': 'g', 'ratio': Fraction(55, 24)}
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
    },
    'active dry yeast': {
        'g': {
            'conversion': {'unit': 'tsp', 'ratio': Fraction(5, 14)}
        }
    },
    'dark chocolate chips': {
        'g': {
            'conversion': {'unit': 'tsp', 'ratio': Fraction(1, 3)}
        }
    },
    'green onion': {
        'bunch': {
            'conversion': {'unit': '', 'ratio': 7}
        }
    }
}

CONVERSION_SYNONYMS = {
    'onion': ['yellow onion', 'white onion', 'red onion']
}
PLURAL_ENDINGS = ['s', 'es', 'ed']


def get_pluralizations(name):
    names = [name]
    plural_endings = ['s', 'es', 'ed']

    for plural_ending in plural_endings:
        names.append(name + plural_ending)

    return names


for ingredient, synonyms in CONVERSION_SYNONYMS.items():
    for synonym in synonyms:
        MAJOR_VOLUME_WEIGHT_CONVERSIONS.update({synonym: MAJOR_VOLUME_WEIGHT_CONVERSIONS[ingredient]})

for ingredient, conversions in MAJOR_VOLUME_WEIGHT_CONVERSIONS.items():
    for pluralization in get_pluralizations(ingredient):
        MAJOR_VOLUME_WEIGHT_CONVERSIONS.update({pluralization: conversions})

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
