from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import json, random

author = 'Luca Corazzini, Philipp Chapkovski, Valeria Maggian'

doc = """
Generalized Gift Exchange Game
"""


class Constants(BaseConstants):
    name_in_url = 'ggeg'
    players_per_group = None
    num_real_players = 9
    num_rounds = 1
    num_others = num_real_players - 1
    coef = 2
    endowment = 100
    INCORRECT_MSG = 'Controllare le istruzioni e provare a rispondere ancora una volta'
    CQ_CHOICES=(0, 100, 125, 150, 300)

class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.endowment = Constants.endowment

    def group_by_arrival_time_method(self, waiting_players):
        wps = [i for i in waiting_players if i.participant.vars.get('role') == 'voter']
        if len(wps) >= Constants.num_real_players:
            return wps[:Constants.num_real_players]


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    intermediary_payoff = models.CurrencyField(initial=0)
    endowment = models.CurrencyField()
    contribution = models.CurrencyField(min=0, max=Constants.endowment)
    others_contributions = models.CurrencyField()
    to_others = models.CurrencyField()

    def set_to_others(self):
        self.to_others = self.contribution * Constants.coef / (Constants.num_real_players - 1)

    def set_payoff(self):
        self.others_contributions = sum([p.to_others for p in self.get_others_in_group()])
        self.intermediary_payoff = self.endowment - self.contribution + self.others_contributions

    cq_ggeg_1 = models.IntegerField(label="Quale sarà il suo guadagno per il periodo?",
                                    choices=Constants.CQ_CHOICES,
                                    widget=widgets.RadioSelectHorizontal
                                    )
    cq_ggeg_2 = models.IntegerField(label="E il guadagno di un altro membro del suo gruppo?",
                                    choices=Constants.CQ_CHOICES,
                                    widget=widgets.RadioSelectHorizontal
                                    )
    cq_ggeg_3 = models.IntegerField(label="Quale sarà il suo guadagno per il periodo?",
                                    choices=Constants.CQ_CHOICES,
                                    widget=widgets.RadioSelectHorizontal
                                    )

    def cq_ggeg_1_error_message(self, value):
        if value != 0:
            return Constants.INCORRECT_MSG

    def cq_ggeg_2_error_message(self, value):
        if value != 125:
            return Constants.INCORRECT_MSG

    def cq_ggeg_3_error_message(self, value):
        if value != 300:
            return Constants.INCORRECT_MSG
