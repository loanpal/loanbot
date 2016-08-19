from parsers import parse

order = [
    'zipcode',
    'property_value',
    'mortgage_balance',
    'credit_score',
    'dob',
    'bankruptcy_foreclosure',
    'street_address',
    'name',
    'phone_number'
]

details = {
    'zipcode': {
        'questions': ['Lets get started. What is your current zip code?'],
        'data_to_collect': [
            'first_name',
            'last_name'
        ],
        'repeat_questions': [
            'I didn\'t get that, what is your zip code?',
            'I didn\'t recognize your zipcode. Can you type it again? it should be 5 digits.'
        ],
        'should_verify': False,
        'parser': parse,
    },
    'property_value': {
        'questions': ['Please estimate the value of the property.'],
        'data_to_collect': [
            'property_value',
        ],
        'repeat_questions': [
            'I didn\'t get that, what is the value of your property?',
        ],
        'should_verify': False,
        'parser': parse,
    },
    'mortgage_balance': {
        'questions': ['What is the remaining 1st mortgage balance?'],
        'data_to_collect': [
            'mortgage_balance',
        ],
        'repeat_questions': [
            'I didn\'t get that, what is the remaining 1st mortgage balance?',
        ],
        'should_verify': False,
        'parser': parse,
    },
    'credit_score': {
        'questions': ['Estimate your credit score.'],
        'data_to_collect': [
            'credit_score',
        ],
        'repeat_questions': [
            'I didn\'t get that, please estimate your credit score.',
        ],
        'should_verify': False,
        'parser': parse,
    },
    'dob': {
        'questions': ['When were you born?'],
        'data_to_collect': [
            'dob',
        ],
        'repeat_questions': [
            'I didn\'t get that, when were you born?',
        ],
        'should_verify': False,
        'parser': parse,
    },
    'bankruptcy_foreclosure': {
        'questions': ['Have you had a bankruptcy or foreclosure in the last 7 years?'],
        'data_to_collect': [
            'is_recent_bankruptcy',
            'is_recent_foreclosure',
        ],
        'repeat_questions': [
            'I didn\'t get that, have you had a bankruptcy or foreclosure in the last 7 years?',
        ],
        'should_verify': False,
        'parser': parse,
    },
    'street_address': {
        'questions': ['What is your current street address?'],
        'data_to_collect': [
            'street_address',
        ],
        'repeat_questions': [
            'I didn\'t get that, what is your current street address?',
        ],
        'should_verify': False,
        'parser': parse,
    },
    'name': {
        'questions': ['What is your full name?'],
        'data_to_collect': [
            'first_name',
            'last_name',
        ],
        'repeat_questions': [
            'I didn\'t get that, what is your full name?',
        ],
        'should_verify': False,
        'parser': parse,
    },
    'phone_number': {
        'questions': ['Great, your rates are ready. What is your mobile or home phone number?'],
        'data_to_collect': [
            'phone_number',
        ],
        'repeat_questions': [
            'I didn\'t get that, have you had a bankruptcy or foreclosure in the last 7 years?',
        ],
        'should_verify': False,
        'parser': parse,
    },
}
