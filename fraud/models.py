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
    players_per_group = 11
    num_rounds = 10
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
        True: 'commettere broglio elettorale in questo round',
        False: 'NON commettere broglio elettorale in questo round'
    }
    candidate_A_msgs = [
        'Il candidato B ha deciso di commettere broglio elettorale, cioè di togliere un voto al partito Alpha per aggiungerlo al partito Beta.',
        'Il candidato B ha deciso di NON commettere broglio elettorale, cioè di togliere un voto al partito Alpha per aggiungerlo al partito Beta.',
        'Niente da comunicare.'
    ]
    candidate_B_msgs = [
        'Il candidato A ha deciso di commettere broglio elettorale, cioè di togliere un voto al partito Beta per aggiungerlo al partito Alpha.',
        'Il candidato A ha deciso di NON commettere broglio elettorale, cioè di togliere un voto al partito Beta per aggiungerlo al partito Alpha.',
        'Niente da comunicare.'
    ]


class Subsession(BaseSubsession):
    treatment = models.StringField()
    lock = models.BooleanField(initial=True)

    def vars_for_admin_report(subsession):
        payoffs = sorted([p.payoff for p in subsession.get_players()])
        return dict(payoffs=payoffs)

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
        for p in self.session.get_participants():
            if p.vars['role'] == 'candidate':
                p.vars['paying_app'] = 'fraud'
                p.vars['paying_round'] = random.randint(1, Constants.num_rounds)
                p.vars['round_to_show'] = p.vars['paying_round']
            else:
                r = random.randint(1, Constants.num_rounds + 1)
                p.vars['round_to_show'] = r
                if r <= Constants.num_rounds:
                    p.vars['paying_app'] = 'fraud'
                    p.vars['paying_round'] = r
                else:
                    p.vars['paying_app'] = 'ggeg'
                    p.vars['paying_round'] = 1

    def get_conversion_rate(self):
        hund_to_euro = self.session.config.get('real_world_currency_per_point') * 100
        return f'100 points = {hund_to_euro}€'


class Group(BaseGroup):
    fraud_cost = models.IntegerField()
    fraud_A = models.BooleanField(
        label='Scegli se:',
        choices=[
            (False, 'Nessun broglio elettorale: NON togliere un voto all’altro partito per aggiungerlo al tuo'),
            (True, 'Broglio elettorale: Togliere un voto all’altro partito per aggiungerlo al tuo')
        ], widget=widgets.RadioSelectHorizontal)
    fraud_B = models.BooleanField(
        label='Scegli se:',
        choices=[
            (False, 'Nessun broglio elettorale: NON togliere un voto all’altro partito per aggiungerlo al tuo'),
            (True, 'Broglio elettorale: Togliere un voto all’altro partito per aggiungerlo al tuo')
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
            if alpha_votes > 0:
                alpha_votes -= self.fraud_B
            if beta_votes > 0:
                beta_votes -= self.fraud_A
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
    intermediary_payoff = models.CurrencyField(initial=0)
    inner_role = models.StringField()
    y = models.IntegerField()
    party = models.StringField()
    vote = models.BooleanField(
        label='Scegli se:',
        choices=[(False, 'Astenerti'), (True, 'Votare')], widget=widgets.RadioSelectHorizontal)
    fraud = models.BooleanField(
        label='Scegli se:',
        choices=[
            (False, 'Nessun broglio elettorale: NON togliere un voto all’altro partito per aggiungerlo al tuo'),
            (True, 'Broglio elettorale: Togliere un voto all’altro partito per aggiungerlo al tuo')
        ], widget=widgets.RadioSelectHorizontal)
    info = models.IntegerField(
        label='Quale messaggio vuoi inviare ai membri del partito Alpha e del partito Beta?',
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
        self.intermediary_payoff = payoff

    def get_candidate_name(self):
        if self.party == 'ALPHA': return 'A'
        return 'B'

    def get_other_party(self):
        if self.party == 'ALPHA': return 'BETA'
        return 'ALPHA'

    def get_other_candidate_name(self):
        if self.party == 'ALPHA': return 'B'
        return 'A'

    def get_other_candidate_decision(self):
        return Constants.fraud_correspondence[self.other_fraud_committed]

    def info_choices(self):
        choices = [
            (0,
             f'Il candidato {self.get_other_candidate_name()} ha deciso di commettere broglio elettorale, cioè di togliere un voto al partito {self.party} per aggiungerlo al partito {self.get_other_party()}'),
            (1,
             f'Il candidato {self.get_other_candidate_name()} ha deciso di  NON commettere broglio elettorale, cioè di togliere un voto al partito {self.party} per aggiungerlo al partito {self.get_other_party()}'),
            (2, 'Niente da comunicare.')
        ]
        return choices

    # cq_block
    cq_1 = models.IntegerField()
    cq_2 = models.IntegerField()
    cq_3 = models.IntegerField()
    cq_4 = models.IntegerField()

    # BASELINE ONLYE
    cq_5 = models.IntegerField()
    cq_6 = models.IntegerField()
    cq_7 = models.IntegerField()
    cq_8 = models.IntegerField()
    # END OF BASELINE ONLYE
    # FRAUD OR FRAUD+INFO ONLY
    cq_9 = models.IntegerField()
    cq_10 = models.IntegerField()
    cq_11 = models.IntegerField()
    cq_12 = models.IntegerField()

    # END OF FRAUD ONLY
