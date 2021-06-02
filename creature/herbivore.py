import pygame

from creature.entity import Entity
from creature.features.movement import *
from creature.plants import *


class Herbivore(Entity):

    def __init__(self):
        super().__init__()
        self.type = EntityTypes.HERBIVORE

    def update(self, dt, entities, steering=None) -> None:
        steering = pg.Vector2()

        food: Set[Movement] = Plant.food_position.query(self.movement)
        food: List[Entity] = [x.parent for x in food]

        target = self.select_closest_creature(food)

        if target is not None:
            steering += self.movement.go_to([target])

        super(Herbivore, self).update(dt, entities, steering)

        for plant in food:
            if plant.movement.position.distance_to(self.movement.position) < self.eat_range:
                Plant.food_position.remove(plant.movement, Plant.food_position.key(plant.movement))
                plant.is_ded = True

    pass
