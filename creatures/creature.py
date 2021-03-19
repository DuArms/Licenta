from creatures.features.movement import Movement
from resurse.constants import *
from typing import List , Set


# tasks : comportament agro , friendly
# chense to survice
# viziuni viteza food strenght
# intelect


class Creature:

    def __init__(self, gen=True):
        if gen is True:
            self.movement = Movement()

            self.vizion = MAP_RANGE

            self.eat_range = 30

            self.dead = False
            self.food = False

    def __repr__(self):
        return f"""({self.movement}\t{self.food}) \n"""

    def get_coord(self):
        return np.asarray((self.movement.x, self.movement.y))


# End of class
TypeCreatureList = List[Creature]

populations: TypeCreatureList = [
    Creature() for _ in range(10)
]






def to_draw():
    vizion_circle = []
    direction_momentum = []
    for creature in populations:
        vizion_circle.append([creature.get_coord(), creature.vizion])
        direction_momentum.append([creature.get_coord(), creature.get_coord() + creature.movement.momentum * 10])

    return zip (vizion_circle, direction_momentum)


if __name__ == "__main__":
    print(populations)
