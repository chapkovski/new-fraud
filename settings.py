from os import environ

SESSION_CONFIGS = [
    dict(
        name='ggeg_only',
        display_name="GGEG Only",
        num_demo_participants=3,
        app_sequence=['ggeg'],
    ),
    dict(
        name='baseline_voter',
        display_name="Baseline: VOTER",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=False,
        info=False,
        role='voter'
    ),
    dict(
        name='baseline_candidate',
        display_name="Baseline: CANDIDATE",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=False,
        info=False,
        role='candidate'
    ),
    dict(
        name='fraud_voter',
        display_name="Fraud: VOTER",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=True,
        info=False,
        role='voter'

    ),
    dict(
        name='fraud_candidate',
        display_name="Fraud: CANDIDATE",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=True,
        info=False,
        role='candidate'
    ),
    dict(
        name='fraudinfo_voter',
        display_name="Fraud + Communication: VOTER",
        num_demo_participants=3,
        app_sequence=['fraud'],
        fraud=True,
        info=True,
        role='voter'
    ),
    dict(
        name='fraudinfo_candidate',
        display_name="Fraud + Communication: CANDIDATE",
        num_demo_participants=4,
        app_sequence=['fraud'],
        fraud=True,
        info=True,
        role='candidate'
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.05, participation_fee=1.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

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
