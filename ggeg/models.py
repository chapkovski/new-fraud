from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Luca Corazzini, Philipp Chapkovski, Valeria Maggian'

doc = """
Generalized Gift Exchange Game
"""


class Constants(BaseConstants):
    name_in_url = 'ggeg'
    players_per_group = 3
    num_rounds = 1
    num_others = players_per_group - 1
    coef = 2
    endowment = 100


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.endowment = Constants.endowment


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    intermediary_payoff = models.CurrencyField(initial=0)
    endowment = models.CurrencyField()
    contribution = models.CurrencyField(min=0, max=Constants.endowment)
    others_contributions = models.CurrencyField()
    to_others = models.CurrencyField()

    def set_to_others(self):
        self.to_others = self.contribution * Constants.coef / (Constants.players_per_group - 1)

    def set_payoff(self):
        self.others_contributions = sum([p.to_others for p in self.get_others_in_group()])
        self.intermediary_payoff = self.endowment - self.contribution + self.others_contributions

    cq_ggeg_1 = models.IntegerField(label="What will be group member A’s final earnings for Part 2?",
                                    choices=(0, 100, 150, 200, 300),
                                    widget=widgets.RadioSelectHorizontal
                                    )
    cq_ggeg_2 = models.IntegerField(label="What will be A’s in group members’ final earnings for Part 2?",
                                    choices=(0, 100, 150, 200, 300),
                                    widget=widgets.RadioSelectHorizontal
                                    )
    cq_ggeg_3 = models.IntegerField(label="What will be subject A’s final earnings for Part 2?",
                                    choices=(0, 50, 100, 200, 300),
                                    widget=widgets.RadioSelectHorizontal
                                    )
