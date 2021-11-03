from markupsafe import escape, Markup


class Constants(BaseConstants):
    name_in_url = 'Instructions'
    players_per_group = None
    num_rounds = 1
    endowment = 10

    CQ_PARTIES_CHOICES = [(4, '4'), (5, '5'), (9, '9')]
    CQ_POINTS_B_CHOICES = [(5, '5'), (21, '21'), (26, '26'), (55, '55'), (76, '76'), (105, '105')]
    CQ_POINTS_A_CHOICES = [(5, '5'), (60, '60'), (70, '70'), (110, '110'), (170, '170'), (210, '210')]

    YES_NO_CHOICES = [(1, 'Yes'), (0, 'No')]
