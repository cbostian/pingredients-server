ADDITIVE_CONJUNCTIONS = ['and', '&']
EXCLUSIVE_CONJUNCTIONS = ['or', '/']

INGREDIENT_COMMON_ADJECTIVES = {
    'pepper': ['black', 'cracked'],
    'garlic': [],
    'chili flake': ['red'],
    'pumpkin': ['canned'],
    'flour': ['all-purpose'],
    'salt': ['kosher'],
    'oil': ['olive', 'cooking'],
    'parmesan cheese': ['grated'],
    'kale': ['leaves'],
    'onion': ['yellow'],
    'broth': ['vegetable'],
    'curry powder': [],
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
}

PREFERRED_NAME_OVERRIDES = {
    'broth': 'vegetable broth',
    'oil': 'olive oil',
    'onion': 'yellow onion',
    'potato': 'russet potato',
    'cheese': 'cheddar cheese',
    'shredded cheese': 'shredded cheddar cheese'
}

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
    '.'
]

IRRELEVANT_INGREDIENTS = [
    'n/a',
    'water',
    'ice water'
]

UNITS = {
    'oz': {
        'synonyms': ['ounce'],
        'major_to_minor': {}
    },
    'lb': {
        'synonyms': [],
        'major_to_minor': {}
    },
    'tsp': {
        'synonyms': ['teaspoon'],
        'major_to_minor': {}
    },
    'cup': {
        'synonyms': ['c'],
        'major_to_minor': {}
    },
    'dash': {
        'synonyms': [],
        'major_to_minor': {}
    },
    'jar': {
        'synonyms': [],
        'major_to_minor': {}
    },
    'tbsp': {
        'synonyms': ['tablespoon'],
        'major_to_minor': {'unit': 'tsp', 'ratio': 3.0}
    },
    'ml': {
        'synonyms': [],
        'major_to_minor': {}
    },
    'g': {
        'synonyms': [],
        'major_to_minor': {}
    },
    'head': {
        'synonyms': [],
        'major_to_minor': {}
    },
    'can': {
        'synonyms': [],
        'major_to_minor': {}
    },
    'clove': {
        'synonyms': [],
        'major_to_minor': {}
    }
}

ALL_DERIVED_UNITS = []
for unit, unit_properties in UNITS.items():
    ALL_DERIVED_UNITS += [unit] + unit_properties['synonyms']

