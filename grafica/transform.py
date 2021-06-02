from creature.features.movement import Movement
from creature.entity import Entity
from creature.carnivore import Carnivore
from creature.plants import Plant
from creature.herbivore import Herbivore
from res.const import *
from time import sleep

import pygame as pg
import copy

size = 20
neutral_creature = pg.Surface((size, size), pg.SRCALPHA)
pg.draw.polygon(neutral_creature, pg.Color('blue'),
                [(0, size * 0.25), (0, size * 0.75), (size, size / 2)])

hostile_creature = pg.Surface((size, size), pg.SRCALPHA)
pg.draw.polygon(hostile_creature, pg.Color('red'),
                [(0, size * 0.25), (0, size * 0.75), (size, size / 2)])

plant_img = pg.Surface((size, size), pg.SRCALPHA)
pg.draw.circle(plant_img, pg.Color('green'),
               (size / 2, size / 2), size / 3)

pop = []

plants = []


class ScreenObject(pg.sprite.Sprite):
    debug = False

    def __init__(self, object: Movement, image):
        super().__init__()
        self.og_imagine = image
        self.pointer_object = object
        self.image = image
        self.rect = self.image.get_rect(center=self.pointer_object.position)

        pass

    def update(self) -> None:
        self.image = pg.transform.rotate(self.og_imagine, -self.pointer_object.heading)
        self.rect = self.image.get_rect(center=self.pointer_object.position)

        if ScreenObject.debug:
            center = pg.Vector2((MAX_PERCEPTION, MAX_PERCEPTION))

            velocity = pg.Vector2(self.pointer_object.velocity)
            velocity += center

            acceleration = pg.Vector2(self.pointer_object.acceleration)
            acceleration += center

            steering = pg.Vector2(self.pointer_object.steering)
            steering += center

            overlay = pg.Surface((MAX_PERCEPTION * 2, MAX_PERCEPTION * 2), pg.SRCALPHA)

            overlay.blit(self.image, self.image.get_rect(center=center))
            #
            # pg.draw.line(overlay, pg.Color('green'), center, velocity, 3)
            #
            # pg.draw.line(overlay, pg.Color('red'), center,
            #              acceleration, 3)
            #
            # pg.draw.line(overlay, pg.Color('blue'), center,
            #              steering, 3)

            pg.draw.circle(overlay, pg.Color('green'), center,
                           self.pointer_object.perception, 2)

            #
            # pg.draw.circle(overlay, pg.Color('red'), center,
            #                1, 2)

            # draw field of view lines

            def field_of_view_line(sign):
                sight = copy.deepcopy(self.pointer_object.velocity)
                _, angle = sight.as_polar()

                sight.from_polar((self.pointer_object.perception, angle + sign * self.pointer_object.field_of_view))
                sight += center

                pg.draw.line(overlay, pg.Color('pink'), center,
                             sight, 1)

            field_of_view_line(1)
            field_of_view_line(-1)

            self.image = overlay
            self.rect = overlay.get_rect(center=self.pointer_object.position)
        else:
            self.rect = self.image.get_rect(center=self.pointer_object.position)




for _ in range(200):
    entity = Herbivore()
    entity.to_draw = ScreenObject(entity.movement, neutral_creature)
    pop.append(entity)

for _ in range(10):
    entity = Carnivore()
    entity.to_draw = ScreenObject(entity.movement, hostile_creature)
    pop.append(entity)

for _ in range(1000):
    entity = Plant()
    entity.to_draw = ScreenObject(entity.movement, plant_img)
    plants.append(entity)

