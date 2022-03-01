from otree.api import Currency as c, currency_range
from ._builtin import WaitPage
from fraud.pages import Page
from .models import Constants, Player
import json

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
        self.player.set_payoffs()


class Results(Page):
    def vars_for_template(self) -> dict:

        return {'others': sum(json.loads(self.player.others_contributions)),
                'your_share_of_others':round(sum(json.loads(self.player.others_contributions))/Constants.num_others)}


page_sequence = [
    SecondPartIntro,
    AnnouncingSecondPart,
    ComprehensionQ,
    Contribution,

    Results
]
