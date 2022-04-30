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
    alpha_party = 'ALPHA'
    beta_party = 'BETA'
    parties = [alpha_party, beta_party]
    num_alpha = 4
    num_beta = 5
    voters = [alpha_party] * num_alpha + [beta_party] * num_beta
    candidate_ids = [10, 11]
    fraud_costs = [20, 40]
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

    def creating_session(self):

        for p in self.get_players():
            if p.id_in_group in Constants.candidate_ids:
                p.inner_role = 'candidate'
                p.participant.vars['role'] = 'candidate'
            else:
                p.inner_role = 'voter'
                p.participant.vars['role'] = 'voter'
            p.save()

        if self.session.config.get('fraud') and self.session.config.get('info'):
            self.treatment = 'fraud_info'
        elif self.session.config.get('fraud') and not self.session.config.get('info'):
            self.treatment = 'fraud_only'
        else:
            self.treatment = 'baseline'

        if self.round_number == 1:
            for g in self.get_groups():
                for i, p in enumerate(g.candidates):
                    p.participant.vars['party'] = Constants.parties[i]
        for g in self.get_groups():
            g.fraud_cost = random.choice(Constants.fraud_costs)
            voters = Constants.voters.copy()
            # random.shuffle(voters)
            for i, p in enumerate(g.voters):
                p.y = random.randint(Constants.lby, Constants.uby)

                p.party = voters[i]

            for p in g.candidates:
                p.party = p.participant.vars.get('party')

    def get_conversion_rate(self):
        hund_to_euro = self.session.config.get('real_world_currency_per_point') * 100
        return f'100 points = {hund_to_euro}€'


class Group(BaseGroup):
    fraud_cost = models.IntegerField()
    fraud_A = models.BooleanField(
        label='Please, make your decision for this round:',
        choices=[
            (False, 'Not implement the electoral fraud'),
            (True, 'Implement the electoral fraud')
        ], widget=widgets.RadioSelectHorizontal)
    fraud_B = models.BooleanField(
        label='Please, make your decision for this round:',
        choices=[
            (False, 'Not implement the electoral fraud'),
            (True, 'Implement the electoral fraud')
        ], widget=widgets.RadioSelectHorizontal)

    party_win = models.StringField()
    voters_informed = models.BooleanField()
    candidate_A_msg = models.StringField()
    candidate_B_msg = models.StringField()

    @property
    def candidates(self):
        return self.player_set.filter(inner_role='candidate')

    @property
    def voters(self):
        return self.player_set.filter(inner_role='voter')

    def set_winner_party(self):
        voters = self.player_set.filter(inner_role='voter')
        alpha_votes = voters.filter(party=Constants.alpha_party).count()
        beta_votes = voters.filter(party=Constants.beta_party).count()
        if self.session.config.get('fraud'):
            alpha_votes += self.fraud_A
            beta_votes += self.fraud_B
        if alpha_votes > beta_votes:
            self.party_win = Constants.alpha_party

        elif alpha_votes < beta_votes:
            self.party_win = Constants.beta_party
        else:
            self.party_win = random.choice(Constants.parties)

    def set_payoffs(self):
        for p in self.get_players():
            p.set_payoff()


class Player(BasePlayer):
    inner_role = models.StringField()
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

    @property
    def fraud(self):
        if self.party == Constants.alpha_party:
            return self.group.fraud_A
        else:
            return self.group.fraud_B

    @property
    def other_fraud_committed(self):
        if self.party == Constants.alpha_party:
            return self.group.fraud_B
        else:
            return self.group.fraud_A

    def role(self):
        return self.inner_role

    def set_payoff(self):
        if self.role() == 'voter':
            payoff = self.y
            if self.group.party_win == self.party:
                payoff += Constants.payoffs['voter']['win']
            else:
                payoff += Constants.payoffs['voter']['loss']
            payoff -= (self.y) * self.vote
            # print(f'y:{self.y}, current payoff:{payoff}, vote:{self.vote}, diff to payoff: {self.y*self.vote}, party won::{self.group.party_win == self.party}')
            # print('-'*100)
        else:
            if self.group.party_win == self.party:
                payoff = Constants.payoffs['candidate']['win']
            else:
                payoff = Constants.payoffs['candidate']['loss']
            if self.session.config.get('fraud'):
                payoff -= (self.group.fraud_cost) * self.fraud
        self.payoff = payoff

    def get_candidate_name(self):
        if self.party == 'ALPHA': return 'A'
        return 'B'

    def get_other_candidate_name(self):
        if self.party == 'ALPHA': return 'B'
        return 'A'

    def get_other_candidate_decision(self):
        return Constants.fraud_correspondence[self.other_fraud_committed]

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
    # FRAUD OR FRAUD+INFO ONLY
    cq_8 = models.IntegerField(
        label="""Suppose the following situation: In a round the cost of electoral fraud is equal to 40 points. Both Candidate A and Candidate B decide not to implement electoral fraud. A member of the BETA party is randomly assigned a Y bonus equal to 21 points and decides to abstain. In Total, three members of the BETA party and four members of the ALPHA party chose to vote. How many points does the above described member of the BETA party earn in this round?""",
        choices=[5, 21, 26, 55, 76, 105],
        widget=widgets.RadioSelect
    )
    cq_9 = models.IntegerField(
        label="""Suppose the following situation: In a round the cost of electoral fraud is equal to 40 points. Both Candidate A and Candidate B decide not to implement electoral fraud. In Total, four members of the Beta party and four members of the Alpha party decide to vote. How many points does Candidate A earn in this round?""",
        choices=[5, 60, 70, 110, 170, 210],
        widget=widgets.RadioSelect
    )
    cq_10 = models.IntegerField(
        label="""Suppose the following situation: In a round the cost of electoral fraud is equal to 20 points. Candidate A decides to implement electoral fraud while Candidate B does not. In Total, four members of the Beta party and four members of the Alpha party decide to vote. How many points does Candidate A earn in this round?""",
        choices=[5, 60, 70, 110, 190, 210],
        widget=widgets.RadioSelect
    )
    cq_11 = models.IntegerField(label="""How many points does Candidate B earn in this round?""",
                                choices=[5, 60, 70, 110, 170, 210],
                                widget=widgets.RadioSelect
                                )

    # END OF FRAUD ONLY
