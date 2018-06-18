ADDITIVE_CONJUNCTIONS = ['and', '&']
EXCLUSIVE_CONJUNCTIONS = ['or', '/']
CONDITIONAL_CONJUNCTIONS = ['if']

INGREDIENT_COMMON_ADJECTIVES = {
    'pepper': ['black', 'cracked'],
    'chili flake': ['red'],
    'flour': ['all purpose'],
    'salt': ['kosher'],
    'oil': ['olive', 'cooking'],
    'parmesan cheese': ['grated'],
    'kale': ['leaves'],
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
    'coriander': ['ground'],
    'cinnamon': ['ground'],
    'chickpeas': ['canned'],
    'lentils': ['red'],
    'maple': ['syrup'],
    'coconut oil': ['virgin']
}

INGREDIENT_SYNONYMS = {
    'coriander': 'cilantro',
    'confectioners sugar': 'powdered sugar'
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
    'with',
    'stems',
    'removed',
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
    'thai'
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
        'conversion': {'unit': 'tbsp', 'ratio': 16.0}
    },
    'dash': {
        'synonyms': [],
        'conversion': {'unit': 'tsp', 'ratio': 1.0 / 8.0}
    },
    'jar': {
        'synonyms': [],
        'conversion': {}
    },
    'tbsp': {
        'synonyms': ['tablespoon'],
        'conversion': {'unit': 'tsp', 'ratio': 3.0}
    },
    'ml': {
        'synonyms': [],
        'conversion': {}
    },
    'g': {
        'synonyms': [],
        'conversion': {}
    },
    'head': {
        'synonyms': [],
        'conversion': {}
    },
    'can': {
        'synonyms': [],
        'conversion': {'unit': 'oz', 'ratio': 14.0}
    },
    'clove': {
        'synonyms': [],
        'conversion': {}
    },
    'sheet': {
        'synonyms': [],
        'conversion': {}
    },
}

ALL_DERIVED_UNITS = []
for unit, unit_properties in UNITS.items():
    ALL_DERIVED_UNITS += [unit] + unit_properties['synonyms']

