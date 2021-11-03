from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'Instructions'
    players_per_group = None
    num_rounds = 1
    endowment = 10

    CQ_1 = models.IntegerField(label=_('How many members are in the Alpha party?'),
                               choices=Constants.CQ_PARTIES_CHOICES, widget=widgets.RadioSelect)
    CQ_2 = models.IntegerField(label=_('How many members are in the Beta party?'),
                               choices=Constants.CQ_PARTIES_CHOICES, widget=widgets.RadioSelect)
    CQ_3 = models.IntegerField(label=_('Is the role of member of party ALPHA or BETA randomly assigned in each round?'),
                               choices=Constants.YES_NO_CHOICES, widget=widgets.RadioSelect)
    CQ_4 = models.IntegerField(label=_('Is the role of candidate A and B randomly assigned in each round?'),
                               choices=Constants.YES_NO_CHOICES, widget=widgets.RadioSelect)
    CQ_5 = models.IntegerField(
        label=_('Is the Y bonus of one party member necessarily the same as other members of the same party?'),
        choices=Constants.YES_NO_CHOICES, widget=widgets.RadioSelect)
    CQ_6 = models.IntegerField(label=_(
        'Suppose in round 3 you are randomly assigned to be a member of the Beta party. Moreover, suppose your randomly assigned Y bonus in this round is equal to 21 points. Suppose you choose to abstain. Totally (you are included), three members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round?'),
        choices=Constants.CQ_POINTS_B_CHOICES, widget=widgets.RadioSelect)
    CQ_7 = models.IntegerField(label=_(
        'Suppose in round 3 you are randomly assigned to be a member of the Beta party. Moreover, suppose your randomly assigned Y bonus in this round is equal to 21 points. Suppose you choose to vote. Totally (you are included), four members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round? '),
        choices=Constants.CQ_POINTS_B_CHOICES, widget=widgets.RadioSelect)
    CQ_8 = models.IntegerField(label=_(
        'Suppose you are randomly assigned the role of Candidate A. Moreover, suppose the cost of electoral fraud in this round is equal to 40 points. Suppose you and candidate B both decide not to implement electoral fraud. Totally, four members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round?'),
        choices=Constants.CQ_POINTS_A_CHOICES, widget=widgets.RadioSelect)
    CQ_9 = models.IntegerField(label=_(
        'Suppose you are randomly assigned the role of Candidate A. Moreover, suppose the cost of electoral fraud in this round is equal to 40 points. Suppose you and candidate B both decide not to implement electoral fraud. Totally, four members of the Beta party and four members of the Alpha party chose to vote. How many points does candidate B earn in this round??'),
        choices=Constants.YES_NO_CHOICES, widget=widgets.RadioSelect)
    CQ_10 = models.IntegerField(label=_(
        'Suppose you are randomly assigned the role of Candidate A. Moreover, suppose the cost of electoral fraud in this round is equal to 40 points. Suppose you decide to implement electoral fraud while candidate B does not. Totally, four members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round?'),
        choices=Constants.YES_NO_CHOICES, widget=widgets.RadioSelect)
    CQ_11 = models.IntegerField(label=_(
        'Suppose you are randomly assigned the role of Candidate A. Moreover, suppose the cost of electoral fraud in this round is equal to 40 points. Suppose you and candidate B both decide not to implement electoral fraud. Totally, four members of the Beta party and four members of the Alpha party chose to vote. How many points does candidate B earn in this round?'),
        choices=Constants.YES_NO_CHOICES, widget=widgets.RadioSelect)
