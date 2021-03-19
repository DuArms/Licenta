from resurse.constants import *
from creatures.creature import TypeCreatureList


def get_food(creatures: TypeCreatureList):
    return list(filter(lambda cr: cr.food, creatures))


def distance(c1, c2):
    return np.linalg.norm(c1 - c2)
