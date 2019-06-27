from itertools import product


def simple_product(players):
    return filter(lambda x: x[0] != x[1], product(players, players))
