import numpy as np
from typing import List

from creatures.creature import *
from creatures.food import *

from resurse.constants import *
from quality_of_life.commom_algs import *
from quality_of_life.commom_algs import *


class World:
    def __init__(self):
        self.length = MAP_SIZE
        self.radius = MAP_RANGE
        self.creatures: TypeCreatureList = populations

    def get_near_creatures(self, creature: Creature, creature_list: TypeCreatureList = None) -> TypeCreatureList:
        if creature_list is None:
            creature_list = self.creatures

        coord = creature.get_coord()
        neighborhood = []

        for cr in creature_list:
            if cr == creature:
                continue

            coord_peer = cr.get_coord()

            if distance(coord, coord_peer) < creature.vizion:
                neighborhood.append(cr)

        return neighborhood


def tick():
    food_global = food_supply

    for creature in world.creatures:

        food_local = list( world.get_near_creatures(creature, food_global) )

        if food_local:
            dist_food = [distance(f.get_coord(), creature.get_coord()) for f in food_local]
            closest_food_index = np.argmin(dist_food)

            picked_food = food_local[closest_food_index]

            if dist_food[closest_food_index] < creature.eat_range:
                picked_food.dead = True
                food_global.remove(picked_food)

            creature.movement.move(picked_food.get_coord())
        else:
            creature.movement.move()

    for food in food_global:
        food.movement.move()

    for pop in populations:
        if pop.dead:
            populations.remove(pop)

    food_global |= {Food() for _ in range(MAX_FOOD - len(food_global))}


world = World()

if __name__ == "__main__":
    a = world.get_near_creatures(populations[0])

a = get_food(populations)

print(a)
