from otree.api import Currency as c, currency_range
from .pages import *
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        if self.participant.vars.get('role')=='voter':
            yield SecondPartIntro,

            yield AnnouncingSecondPart,
            yield ComprehensionQ, {
                        'cq_ggeg_1': 0,
                        'cq_ggeg_2': 150,
                        'cq_ggeg_3': 300,
                    },

            yield Contribution, {'contribution': random.randint(0, self.player.endowment)}
            yield Results

