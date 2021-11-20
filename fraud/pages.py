from otree.api import Currency as c, currency_range
from ._builtin import Page as oTreePage, WaitPage
from .models import Constants


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
    form_model = 'player'

    def get_form_fields(self):
        qs = [f'cq_{i}' for i in range(1, 8)]
        if self.subsession.treatment != 'baseline':
            toadd = [f'cq_{i}' for i in range(8, 12)]
            qs.extend(toadd)
        return qs


page_sequence = [
    Introduction,
    Instructions,
    EarningsIntro,
    EarningsMembersExplained,
    EarningsCandidatesExplained,
    Examples,
    QuizAnnouncement,
    Quiz,

]
