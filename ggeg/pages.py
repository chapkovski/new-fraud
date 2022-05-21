from otree.api import Currency as c, currency_range
from ._builtin import WaitPage
from fraud.pages import Page as FraudPage
from .models import Constants, Player
import json

class Page(FraudPage):
    def is_displayed(self):
        return self.participant.vars.get('role') != 'candidate'

class FirstWP(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return self.participant.vars.get('role') != 'candidate'


class SecondPartIntro(Page):
    pass


class AnnouncingSecondPart(Page):
    pass


class ComprehensionQ(Page):
    form_model = 'player'
    form_fields = [
        "cq_ggeg_1",
        "cq_ggeg_2",
        "cq_ggeg_3"
    ]


class Contribution(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def before_next_page(self):
        self.player.set_to_others()


class BeforeResultsWP(WaitPage):
    def is_displayed(self):
        return self.participant.vars.get('role') != 'candidate'

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()


class Results(Page):
    def vars_for_template(self) -> dict:
        return {'others': sum([p.contribution for p in self.player.get_others_in_group()])}


page_sequence = [
    FirstWP,
    # SecondPartIntro,
    # AnnouncingSecondPart,
    ComprehensionQ,
    Contribution,
    BeforeResultsWP,
    Results
]
