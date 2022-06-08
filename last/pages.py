from otree.api import Currency as c, currency_range
from ._builtin import WaitPage
from .models import Constants
from fraud.pages import Page
from pprint import pprint
import json


class Q1(Page):
    def post(self):
        survey_data = json.loads(self.request.POST.get('surveyholder'))
        votare = survey_data.pop('votare', [])

        for k, v in survey_data.items():
            try:
                setattr(self.player, k, int(v))
            except ValueError:
                setattr(self.player, k, v)
            except AttributeError:
                pass

        for i in votare:
            try:
                setattr(self.player, i, True)
            except AttributeError:
                pass
        return super().post()


class Q2(Page):
    def post(self):
        survey_data = json.loads(self.request.POST.get('surveyholder'))
        pprint(survey_data)
        for k, v in survey_data.items():
            try:
                setattr(self.player, k, int(v))
            except ValueError:
                setattr(self.player, k, v)
            except AttributeError:
                pass
        return super().post()


class FinalResults(Page):
    def is_displayed(self):
        return len(self.session.config.app_sequence) > 1

    def vars_for_template(self):
        app_to_pay = self.participant.vars.get('paying_app')
        paying_round = self.participant.vars.get('paying_round')
        if app_to_pay == 'fraud':
            player = self.participant.fraud_player.get(round_number=paying_round, participant=self.participant)
        else:
            player = self.participant.ggeg_player.get(round_number=paying_round, participant=self.participant)
        self.player.payoff = player.intermediary_payoff


page_sequence = [
    Q1,
    Q2,
    FinalResults

]
