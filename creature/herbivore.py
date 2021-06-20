import pygame

from creature.entity import Entity
from creature.features.movement import *
from creature.plants import *


class Herbivore(Entity):

    def __init__(self, add_to_grid=True, generate_gene=True):
        super().__init__(add_to_grid=add_to_grid, generate_gene=generate_gene)
        self.type = EntityTypes.HERBIVORE

        if not generate_gene:
            self.size = Values.SIZE.low
            self.alignment_importance = 1.5

    def update(self, dt, entities, steering=None) -> None:
        if self.is_ded:
            return

        steering = pg.Vector2()

        food: Set[Movement] = Plant.food_position.query(self.movement)
        food: List[Entity] = [x.parent for x in food]

        target = self.select_closest_creature(food)

        if target is not None:
            steering += self.movement.go_to([target])

        super().update(dt, entities, steering)

        for plant in food:
            if plant.movement.position.distance_to(self.movement.position) < self.eat_range:
                Plant.food_position.remove(plant.movement, Plant.food_position.key(plant.movement))
                plant.is_ded = True
                self.score += HERBIVORE_EAT_VALUE

                for her in self.herbivores:
                    her.score += HERBIVORE_EAT_VALUE // 5

