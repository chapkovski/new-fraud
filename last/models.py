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

author = 'Philipp Chapkvoski'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'last'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        self.session.vars['final_results_locked']=True


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ambito_di_studio = models.StringField()
    anno_nascita = models.IntegerField()
    gender = models.StringField()
    negative_reciprocity_1 = models.IntegerField()
    negative_reciprocity_2 = models.IntegerField()
    negative_reciprocity_3 = models.IntegerField()
    positive_reciprocity_a = models.StringField()
    positive_reciprocity_b = models.IntegerField()
    risk_taking = models.IntegerField()
    trust = models.IntegerField()
    votare_diritto = models.BooleanField(initial=False)
    votare_inutile = models.BooleanField(initial=False)
    votare_dovere = models.BooleanField(initial=False)
    votare_importante = models.BooleanField(initial=False)
    WP13427 = models.IntegerField()
    WP13428 = models.IntegerField()
    WP13429 = models.IntegerField()
    WP13430 = models.IntegerField()
    WP13431 = models.IntegerField()
    WP13432 = models.IntegerField()
    WP13433 = models.IntegerField()
    WP13434 = models.IntegerField()
    WP13435 = models.IntegerField()
    WP13436 = models.IntegerField()
    WP13437 = models.IntegerField()
    WP13438 = models.IntegerField()
    WP13439 = models.IntegerField()
    WP13440 = models.IntegerField()
    WP13441 = models.IntegerField()
    WP13442 = models.IntegerField()
    WP13443 = models.IntegerField()
    WP13444 = models.IntegerField()
    WP13445 = models.IntegerField()
    WP13446 = models.IntegerField()
    WP13447 = models.IntegerField()
    WP13448 = models.IntegerField()
    WP13449 = models.IntegerField()
    WP13450 = models.IntegerField()
    WP13451 = models.IntegerField()
    WP13452 = models.IntegerField()
    WP13453 = models.IntegerField()
    WP13454 = models.IntegerField()
    WP13455 = models.IntegerField()
    WP13456 = models.IntegerField()
    WP13457 = models.IntegerField()
