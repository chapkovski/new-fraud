from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            if self.session.config.get('info'):
                yield SecondPartIntro,
            else:
                yield AnnouncingSecondPart,
                yield ComprehensionQInfo, {
                    'cq_ggeg_1': 0,
                    'cq_ggeg_2': 150,
                    'cq_ggeg_3': 300,
                },
                yield BlockerAfterCQInfo,
        yield Contribution, {'contribution': random.randint(0, self.player.endowment)}
        yield Results

