from os import environ
EXTENSION_APPS=['fraud']
REAL_WORLD_CURRENCY_DECIMAL_PLACES = 1
app_sequence = [
    'fraud',
    'ggeg',
    'last'
]
SESSION_CONFIGS = [

    dict(
        name='baseline',
        display_name=" baseline",
        num_demo_participants=11,
        app_sequence=app_sequence,
        fraud=False,
        info=False,

    ),
    dict(
        name='fraud',
        display_name="Fraud",
        num_demo_participants=11,
        app_sequence=app_sequence,
        fraud=True,
        info=False,


    ),
    dict(
        name='fraud_info',
        display_name="Fraud + Communication",
        num_demo_participants=11,
        app_sequence=app_sequence,
        fraud=True,
        info=True,

    ),
    dict(
        name='q',
        display_name=" Questionnaire only",
        num_demo_participants=1,
        app_sequence=['last'],

    ),
]


ROOMS = [
    dict(
        name='frex',
        display_name='FREX room',
        participant_label_file='_rooms/cafoscari.txt',
        # use_secure_urls=True
    ),
]


# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.08, participation_fee=3.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'it'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'ft=z+gl(x&t0-1%jo4!lmkk@vac_u78+-0lnbngwujz@#aaq^l'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'django.contrib.humanize', ]
