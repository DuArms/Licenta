import pygame

from creature.entity import Entity

from Algoritmi.SpatialHash import SpatialHash
from random import uniform
from res.const import *


class Plant(Entity):
    food_position: SpatialHash

    def __init__(self):
        super(Plant, self).__init__(False)

        self.movement.velocity = Vector2((0, 0))
        self.movement.max_speed = 0
        self.movement.perception = 0
        self.type = EntityTypes.PLANT

        self.food_position.insert(self.movement)

    def update(self, dt, entity, steering=None) -> None:
        if self.to_draw is not None:
            self.to_draw.update()


Plant.food_position = SpatialHash(MAX_PERCEPTION * 2)
