from otree.api import Currency as c, currency_range
from ._builtin import  WaitPage
from .models import Constants
from fraud.pages import Page

class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class FinalResults(Page):
    def vars_for_template(self):
        app_to_pay = self.participant.vars.get('paying_app')
        paying_round = self.participant.vars.get('paying_round')
        if app_to_pay =='fraud':
            player = self.participant.fraud_player.get(round_number=paying_round, participant=self.participant)
        else:
            player = self.participant.ggeg_player.get(round_number=paying_round, participant=self.participant)
        self.player.payoff= player.intermediary_payoff




page_sequence = [
    FinalResults
    # MyPage, ResultsWaitPage, Results
]
