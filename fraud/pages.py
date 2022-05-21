from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
from .models import Constants
import json

class Page(oTreePage):
    instructions = False

    def _is_displayed(self):
        return not self.participant.vars.get('blocked') and self.is_displayed()

    def get_context_data(self, **context):
        r = super().get_context_data(**context)
        r['maxpages'] = self.participant._max_page_index
        r['page_index'] = self._index_in_pages
        r['progress'] = f'{int(self._index_in_pages / self.participant._max_page_index * 100):d}'
        r['instructions'] = self.instructions
        return r


class FirstPage(Page):
    def is_displayed(self):
        return self.round_number == 1


class Introduction(FirstPage):
    def vars_for_template(self):
        return dict(fee=self.session.config.get('participation_fee'))


class Instructions(FirstPage):
    pass


class EarningsIntro(FirstPage):
    pass


class EarningsMembersExplained(FirstPage):
    pass


class EarningsCandidatesExplained(FirstPage):
    pass


class Examples(FirstPage):
    pass


class QuizAnnouncement(FirstPage):
    pass


class Quiz(FirstPage):
    instructions = True
    form_model = 'player'
    def vars_for_template(self):
        return dict(NEXT_BTN='Next',
                    REQUIRED_MSG="Please, answer this question")


    def post(self):
        try:
            survey_data = json.loads(self.request.POST.dict().get('surveyholder'))
        except Exception as e:
            print(e)
            return super().post()

        for k, v in survey_data.items():
            try:
                setattr(self.player, k, int(v))
            except AttributeError:
                pass


        return super().post()

class RoleAnnouncement(Page):
    def is_displayed(self):
        return self.round_number == 1

    instructions = True


class Vote(Page):
    form_model = 'player'
    form_fields = ['vote']

    def is_displayed(self):
        return self.player.role() == 'voter'


class BeforeFrWP(WaitPage):
    pass


class Fraud(Page):
    form_model = 'group'
    instructions = True

    def get_form_fields(self):
        if self.player.party == Constants.alpha_party:
            return ['fraud_A']
        else:
            return ['fraud_B']

    def is_displayed(self):
        return self.player.role() == 'candidate' and self.session.config.get('fraud')


class BeforeInfoWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_winner_party()


class Info(Page):
    instructions = True
    form_model = 'player'
    form_fields = ['info']

    def before_next_page(self):
        if self.player.party == Constants.alpha_party:
            self.group.candidate_A_msg = Constants.candidate_A_msgs[self.player.info]
        if self.player.party == Constants.beta_party:
            self.group.candidate_B_msg = Constants.candidate_B_msgs[self.player.info]

    def is_displayed(self):
        return self.player.role() == 'candidate' and self.session.config.get('info')


class BeforeResultsWP(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    instructions = True

    def app_after_this_page(self, upcoming_apps):
        if self.round_number == Constants.num_rounds and self.player.role() == 'candidate':
            return 'last'


page_sequence = [
    # Introduction,
    # Instructions,
    # EarningsIntro,
    # EarningsMembersExplained,
    # EarningsCandidatesExplained,
    # Examples,
    QuizAnnouncement,
    Quiz,
    RoleAnnouncement,
    Fraud,
    BeforeInfoWP,
    Info,
    BeforeFrWP,
    Vote,
    BeforeResultsWP,
    Results,

]
