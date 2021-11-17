from os import environ

SESSION_CONFIGS = [
    dict(
        name='baseline',
        display_name="Baseline",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=False,
        info=False,
    ),
    dict(
        name='fraud',
        display_name="Fraud",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=True,
        info=False,

    ),
    dict(
        name='fraudinfo',
        display_name="Fraud + Communication",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=True,
        info=True,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = 'ft=z+gl(x&t0-1%jo4!lmkk@vac_u78+-0lnbngwujz@#aaq^l'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
