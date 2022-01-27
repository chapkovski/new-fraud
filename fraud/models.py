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
    num_rounds = 5
    endowment = 10
    parties = ['ALPHA', 'BETA']
    fraud_cost = 40
    lby = 0
    uby = 55
    payoffs = dict(
        voter=dict(
            loss=5,
            tie=55,
            win=105
        ),
        candidate=dict(
            loss=60,
            tie=110,
            win=210
        ),
    )
    fraud_correspondence = {
        True: 'Commit a fraud in this round',
        False: 'DO NOT commit a fraud in this round'
    }
    candidate_A_msgs = [
        'Candidate B decided to implement electoral fraud so to subtract one vote from Party ALPHA',
        'Candidate B decided to NOT to implement electoral fraud so to subtract one vote from Party ALPHA',
        'Nothing to communicate'
    ]
    candidate_B_msgs = [
        'Candidate A decided to implement electoral fraud so to subtract one vote from Party BETA',
        'Candidate A decided to NOT to implement electoral fraud so to subtract one vote from Party BETA',
        'Nothing to communicate'
    ]


class Subsession(BaseSubsession):
    treatment = models.StringField()
    # NB! TODO THAT IS FOR DEBUGGING ONLY - MOVE TO GROUPS!!!
    other_fraud_committed = models.BooleanField()
    party_win = models.StringField()
    voters_informed = models.BooleanField()
    candidate_A_msg = models.StringField()
    candidate_B_msg = models.StringField()

    # END OF THAT IS FOR DEBUGGING ONLY - MOVE TO GROUPS!!!
    def creating_session(self):
        self.candidate_A_msg = random.choice(Constants.candidate_A_msgs)
        self.candidate_B_msg = random.choice(Constants.candidate_B_msgs)
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
        self.party_win = random.choice(Constants.parties)
        if self.session.config.get('role') == 'voter':

            self.voters_informed = random.choice([True, False])
            for p in self.get_players():
                p.y = random.randint(Constants.lby, Constants.uby)
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
    def set_payoffs(self):
        # todo; for debugging only
        if self.role() == 'voter':
            payoff = self.y
            if self.subsession.party_win == self.party:
                payoff += Constants.payoffs['voter']['win']
            else:
                payoff += Constants.payoffs['voter']['loss']
            payoff -= (self.y) * self.vote
        else:
            if self.subsession.party_win == self.party:
                payoff = Constants.payoffs['candidate']['win']
            else:
                payoff = Constants.payoffs['candidate']['loss']
            payoff -= (Constants.fraud_cost) * self.fraud
        self.payoff = payoff

    def role(self):
        return self.session.config.get('role')

    y = models.IntegerField()
    party = models.StringField()
    vote = models.BooleanField(
        label='Please make the decision, whether to vote or abstain in this round:',
        choices=[(False, 'ABSTAIN'), (True, 'VOTE')], widget=widgets.RadioSelectHorizontal)
    fraud = models.BooleanField(
        label='Please, make your decision for this round:',
        choices=[
            (False, 'Not implement the electoral fraud'),
            (True, 'Implement the electoral fraud')
        ], widget=widgets.RadioSelectHorizontal)
    info = models.IntegerField(
        label='Please, choose the message you would like to send to the voters:',
        widget=widgets.RadioSelect)

    def get_candidate_name(self):
        if self.party == 'ALPHA': return 'AB'
        return 'B'

    def get_other_candidate_name(self):
        if self.party == 'ALPHA': return 'B'
        return 'A'

    def get_other_candidate_decision(self):
        return Constants.fraud_correspondence[self.subsession.other_fraud_committed]

    def info_choices(self):
        choices = [
            (0,
             f'Candidate {self.get_other_candidate_name()} decided to implement electoral fraud so to subtract one vote from Party {self.party}'),
            (1,
             f'Candidate {self.get_other_candidate_name()} decided NOT implement  electoral fraud so to subtract one vote from Party {self.party}'),
            (2, 'Nothing to communicate')
        ]
        return choices

    # cq_block
    cq_1 = models.IntegerField(label='How many members are in the ALPHA party?',
                               choices=[4, 5, 9],
                               widget=widgets.RadioSelect)
    cq_2 = models.IntegerField(label='How many members are in the BETA party?',
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

    # BASELINE ONLYE
    cq_6 = models.IntegerField(label="""Suppose the following situation: <br>  In round 3 a member of the BETA  party is randomly assigned a Y bonus equal to 21 points and decides to abstain.<br>
Totally, three members of the BETA party and four members of the ALPHA party choose to vote. How many points does the above described member of the BETA party earn in this round?""",
                               choices=[5, 21, 26, 55, 76, 105],
                               widget=widgets.RadioSelect
                               )
    cq_7 = models.IntegerField(label="""Suppose the following situation: <br>  In round 3 a member of the BETA  party is randomly assigned a Y bonus equal to 21 points and decides to vote.<br>
Totally, three members of the BETA party and four members of the ALPHA party choose to vote. How many points does the above described member of the BETA party earn in this round?""",
                               choices=[5, 21, 26, 55, 76, 105],
                               widget=widgets.RadioSelect
                               )

    # END OF BASELINE ONLYE
    # FRAUD ONLY
    cq_8 = models.IntegerField(label="""Suppose the following situation: 
In round 3 the cost of electoral fraud is equal to 40 points. Both Candidate A and Candidate B decides not to implement electoral fraud. 
A member of the BETA party is randomly assigned a Y bonus equal to 21 points and decides to abstain.
Totally, three members of the BETA party and four members of the ALPHA party choose to vote. How many points does the above described member of the BETA party earn in this round?
""",
                               choices=[5, 21, 26, 55, 76, 105],
                               widget=widgets.RadioSelect
                               )
    cq_9 = models.IntegerField(label="""
   Suppose the following situation: 
In round 3 the cost of electoral fraud is equal to 40 points. Both Candidate A and Candidate B decides not to implement electoral fraud. 
Totally, four members of the Beta party and four members of the Alpha party decide to vote. How many points does Candidate A  earn in this round?
""",
                               choices=[5, 60, 70, 110, 170, 210],
                               widget=widgets.RadioSelect
                               )
    cq_10 = models.IntegerField(label="""Suppose the following situation: 
In round 3 the cost of electoral fraud is equal to 20 points. Candidate A decides to implement electoral fraud  while Candidate B does not. 
Totally, four members of the Beta party and four members of the Alpha party decide to vote. How many points does Candidate A earn in this round?

""",
                                choices=[5, 60, 70, 110, 190, 210],
                                widget=widgets.RadioSelect
                                )
    cq_11 = models.IntegerField(label="""
      How many points does Candidate B earn in this round?""",
                                choices=[5, 60, 70, 110, 170, 210],
                                widget=widgets.RadioSelect
                                )

    # END OF FRAUD ONLY
    # FRAUD + INFO
    cq_12 = models.IntegerField(label="""Suppose the following situation: 
In round 3 the cost of electoral fraud is equal to 40 points. Both Candidate A and Candidate B decides not to implement electoral fraud. Candidate A sends the message “Nothing to communicate” while Candidate B send the message “Candidate A decided to implement electoral fraud so to subtract one vote from Party ALPHA”
A member of the BETA party is randomly assigned a Y bonus equal to 21 points and decides to abstain.
Totally, three members of the BETA party and four members of the ALPHA party choose to vote. How many points does the above described member of the BETA party earn in this round?

    """,
                                choices=[5, 21, 26, 55, 76, 105],
                                widget=widgets.RadioSelect
                                )
    cq_13 = models.IntegerField(label="""Suppose the following situation: 
In round 3 the cost of electoral fraud is equal to 40 points. Both Candidate A and Candidate B decide not to implement electoral fraud. Candidate A sends the message “Candidate B decided to implement electoral fraud so to subtract one vote from Party ALPHA” while Candidate B send the message “Nothing to communicate”
Totally, four members of the Beta party and four members of the Alpha party decide to vote. How many points does Candidate A  earn in this round?

    """,
                                choices=[5, 60, 70, 110, 170, 210],
                                widget=widgets.RadioSelect
                                )
    cq_14 = models.IntegerField(label="""Suppose the following situation: 
In round 3 the cost of electoral fraud is equal to 20 points. Candidate A decides to implement electoral fraud while Candidate B does not. Both candidates send the message “Nothing to communicate”.
Totally, four members of the Beta party and four members of the Alpha party chose to vote. How many points does Candidate A earn in this round?""",
                                choices=[5, 60, 70, 110, 190, 210],
                                widget=widgets.RadioSelect
                                )
    cq_15 = models.IntegerField(label="""
          How many points does Candidate B earn in this round?""",
                                choices=[5, 60, 70, 110, 170, 210],
                                widget=widgets.RadioSelect
                                )
    # END OFFRAUD + INFO
