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
import random, json

author = 'Philipp Chapkovski, HSE-Moscow'

doc = """
Fraud expectations. Maggian, Baghdasaryan, Chapkovski
"""


class Constants(BaseConstants):
    name_in_url = 'fraud'
    players_per_group = None
    num_rounds = 1
    endowment = 10
    parties = ['ALPHA', 'BETA']


class Subsession(BaseSubsession):
    treatment = models.StringField()
    # NB! TODO THAT IS FOR DEBUGGING ONLY - MOVE TO GROUPS!!!
    other_fraud_committed = models.BooleanField()
    party_win = models.StringField()

    # END OF THAT IS FOR DEBUGGING ONLY - MOVE TO GROUPS!!!
    def creating_session(self):
        if self.session.config.get('fraud') and self.session.config.get('info'):
            self.treatment = 'fraud_info'
        elif self.session.config.get('fraud') and not self.session.config.get('info'):
            self.treatment = 'fraud_only'
        else:
            self.treatment = 'baseline'
        # TODO: the following for debugging only.
        if self.round_number == 1 and self.session.config.get('role') == 'candidate':
            for p in self.session.get_participants():
                p.vars['party'] = random.choice(Constants.parties)

        if self.session.config.get('role') == 'voter':
            self.party_win = random.choice(Constants.parties)
            for p in self.get_players():
                p.party = random.choice(Constants.parties)
        if self.session.config.get('role') == 'candidate':
            self.other_fraud_committed = random.choice([True, False])
            for p in self.get_players():
                p.party = p.participant.vars.get('party')

    def get_conversion_rate(self):
        hund_to_euro = self.session.config.get('real_world_currency_per_point') * 100
        return f'100 points = {hund_to_euro}€'


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def role(self):
        return self.session.config.get('role')
    party = models.StringField()
    vote = models.BooleanField()
    fraud = models.BooleanField()
    info = models.BooleanField()
    # cq_block
    cq_1 = models.IntegerField(label='How many members are in the Alpha party?',
                               choices=[4, 5, 9],
                               widget=widgets.RadioSelect)
    cq_2 = models.IntegerField(label='How many members are in the Beta party?',
                               choices=[4, 5, 9],
                               widget=widgets.RadioSelect
                               )
    cq_3 = models.IntegerField(label='Is the role of member of party ALPHA or BETA randomly assigned in each round?',
                               choices=[(1, 'Yes'), (0, 'No'), ],
                               widget=widgets.RadioSelect
                               )
    cq_4 = models.IntegerField(label='Is the role of candidate A and B randomly assigned in each round?',
                               choices=[(1, 'Yes'), (0, 'No'), ],
                               widget=widgets.RadioSelect)
    cq_5 = models.IntegerField(
        label='Is the Y bonus of one party member necessarily the same as other members of the same party?',
        choices=[(1, 'Yes'), (0, 'No'), ],
        widget=widgets.RadioSelect)
    cq_6 = models.IntegerField(label="""
    Suppose in round 3 you are randomly assigned to be a member of the Beta party. Moreover, suppose your randomly assigned Y bonus in this round is equal to 21 points.
    <br><b>Suppose you choose to abstain.</b><br>
Totally (you are included), three members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round?""",
                               choices=[5, 21, 26, 55, 76, 105],
                               widget=widgets.RadioSelect
                               )
    cq_7 = models.IntegerField(label="""
       
        <br><b>Suppose you choose to vote.</b><br>
    Totally (you are included), four members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round?""",
                               choices=[5, 21, 26, 55, 76, 105],
                               widget=widgets.RadioSelect
                               )
    cq_8 = models.IntegerField(label="""
Suppose you are randomly assigned the role of Candidate A. Moreover, suppose the cost of electoral fraud in this round is equal to 40 points
            <br><b>Suppose you and candidate B both decide not to implement electoral fraud. </b><br>
        Totally, four members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round?""",
                               choices=[5, 60, 70, 110, 170, 210],
                               widget=widgets.RadioSelect
                               )
    cq_9 = models.IntegerField(label="""
   How many points does candidate B earn in this round?""",
                               choices=[5, 60, 70, 110, 170, 210],
                               widget=widgets.RadioSelect
                               )
    cq_10 = models.IntegerField(label="""
    <b>Suppose you decide to implement electoral fraud while candidate B does not.  </b><br>
            Totally, four members of the Beta party and four members of the Alpha party chose to vote. How many points do you earn in this round?""",
                                choices=[5, 60, 70, 110, 170, 210],
                                widget=widgets.RadioSelect
                                )
    cq_11 = models.IntegerField(label="""
      How many points does candidate B earn in this round?""",
                                choices=[5, 60, 70, 110, 170, 210],
                                widget=widgets.RadioSelect
                                )

    # cq_block END
