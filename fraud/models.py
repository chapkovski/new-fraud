from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Fraud expectations. Maggian, Baghdasaryan, Chapkovski
"""


class Constants(BaseConstants):
    name_in_url = 'fraud'
    players_per_group = None
    num_rounds = 1
    endowment = 10

class Subsession(BaseSubsession):
    def get_conversion_rate(self):
        hund_to_euro =self.session.config.get('real_world_currency_per_point')*100
        return f'100 points = {hund_to_euro}€'


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
