from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random
from .pages import *


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Introduction,
            yield Instructions,
            yield EarningsIntro,
            yield EarningsMembersExplained,
            yield EarningsCandidatesExplained,
            yield Examples,
            yield QuizAnnouncement,
            yield Quiz, {
                'cq_1': '5', 'cq_2': '9', 'cq_3': '0', 'cq_4': '1', 'cq_5': '1', 'cq_8': '5', 'cq_9': '60',
                'cq_10': '60', 'cq_11': '5'}

        yield pages.RoleAnnouncement
        if self.player.role() == 'voter':
            yield pages.Vote, dict(vote=random.choice([True, False]))
        if self.player.role() == 'candidate':
            if self.subsession.treatment != 'baseline':
                if self.player.party == Constants.alpha_party:
                    yield pages.Fraud, dict(fraud_A=random.choice([True, False]))

                else:
                    yield pages.Fraud, dict(fraud_B=random.choice([True, False]))
                if self.subsession.treatment == 'fraud_info':
                    yield pages.Info, dict(info=random.choice([0, 1, 2]))

        yield pages.Results,
