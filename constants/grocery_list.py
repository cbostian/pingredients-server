ADDITIVE_CONJUNCTIONS = ['and', '&']
EXCLUSIVE_CONJUNCTIONS = ['or', '/']

INGREDIENT_COMMON_ADJECTIVES = {
    'pepper': ['black', 'cracked'],
    'garlic': [],
    'chili flake': ['red'],
    'pumpkin': ['canned'],
    'flour': ['all purpose'],
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
    'broth': 'vegetable broth'
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