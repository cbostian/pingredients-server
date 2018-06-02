ADDITIVE_CONJUNCTIONS = ['and', '&']
EXCLUSIVE_CONJUNCTIONS = ['or', '/']

INGREDIENT_COMMON_ADJECTIVES = {
    'pepper': {
        'common_adjectives': ['black', 'cracked']
    },
    'garlic': {
        'units': ['cloves'],
        'common_adjectives': []
    },
    'chili': {
        'common_adjectives': ['red']
    },
    'pumpkin': {
        'common_adjectives': ['canned']
    },
    'flour': {
        'common_adjectives': ['all purpose']
    },
    'salt': {
        'common_adjectives': ['kosher']
    },
    'oil': {
        'common_adjectives': ['olive', 'cooking']
    },
    'parmesan cheese': {
        'common_adjectives': ['grated']
    },
    'kale': {
        'common_adjectives': ['leaves']
    },
    'onion': {
        'common_adjectives': ['yellow']
    },
    'broth': {
        'common_adjectives': ['vegetable']
    },
    'curry powder': {
        'common_adjectives': []
    },
    'paprika': {
        'common_adjectives': ['smoked', 'ground']
    },
    'cumin': {
        'common_adjectives': ['ground', 'powder']
    },
    'egg': {
        'common_adjectives': ['yolk', 'white']
    },
    'sugar': {
        'common_adjectives': ['granulated', 'white']
    },
    'confectioners sugar': {
        'common_adjectives': ['powdered']
    },
    'butter': {
        'common_adjectives': ['unsalted']
    },
    'heavy cream': {
        'common_adjectives': ['whipping']
    },
    'coconut milk': {
        'common_adjectives': ['full fat']
    },
    'cilantro': {
        'common_adjectives': ['leaves']
    },
    'coriander': {
        'common_adjectives': ['ground']
    },
    'cinnamon': {
        'common_adjectives': ['ground']
    },
    'chickpeas': {
        'common_adjectives': ['canned']
    },
    'lentils': {
        'common_adjectives': ['red']
    },
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
    'reduced'
]

VALID_UNITS = ['oz', 'ounce', 'lb', 'tsp', 'teaspoon', 'cup', 'dash', 'jar', 'tbsp', 'tablespoon', 'ml', 'g',
               'head', 'can', 'clove']