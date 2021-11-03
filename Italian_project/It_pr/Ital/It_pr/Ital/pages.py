from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass


class Page_1(Page):
    pass


class Page_2(Page):
    pass


class Parties_Payoffs(Page):
    pass


class Candidates_Payoffs(Page):
    pass


class Example(Page):
    pass


class Conclusion(Page):
    pass


class Stage_2(Page):
    pass

class CQ(Page):
    form_fields = [
        "CQ_1",
        "CQ_2",
        "CQ_3",
        "CQ_4",
        "CQ_5",
        "CQ_6",
        "CQ_7",
        "CQ_8",
        "CQ_9",
        "CQ_10",
        "CQ_11",

    ]

page_sequence = [Introduction, Page_1, Page_2, Parties_Payoffs, Candidates_Payoffs, Example, Conclusion, CQ, Stage_2
                 ]
