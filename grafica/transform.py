from creature.features.movement import Movement
from creature.creature import Creature
from creature.carnivore import Carnivore
from res.const import *

import pygame as pg
import copy

size = 20
neutral_creature = pg.Surface((size, size), pg.SRCALPHA)
pg.draw.polygon(neutral_creature, pg.Color('blue'),
                [(0,size * 0.25) , (0, size * 0.75), (size,size / 2)])

hostile_creature = pg.Surface((size, size), pg.SRCALPHA)
pg.draw.polygon(hostile_creature, pg.Color('red'),
                [(0,size * 0.25) , (0, size * 0.75), (size,size / 2)])

class ScreenObject(pg.sprite.Sprite):
    debug = True

    def __init__(self, object: Movement , image):
        super().__init__()
        self.og_imagine =image
        self.pointer_object = object
        self.image = image
        self.rect = self.image.get_rect(center=self.pointer_object.position)

        pass

    def update(self) -> None:
        self.image = pg.transform.rotate(self.og_imagine , -self.pointer_object.heading)
        self.rect = self.image.get_rect(center=self.pointer_object.position)

        if ScreenObject.debug:
            center = pg.Vector2((MAX_PERCEPTION, MAX_PERCEPTION))

            velocity = pg.Vector2(self.pointer_object.velocity)
            speed = velocity.length()
            velocity += center

            acceleration = pg.Vector2(self.pointer_object.acceleration)
            acceleration += center

            steering = pg.Vector2(self.pointer_object.steering)
            steering += center

            overlay = pg.Surface(( MAX_PERCEPTION * 2,  MAX_PERCEPTION * 2), pg.SRCALPHA)

            overlay.blit( self.image, self.image.get_rect(center=center))
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

            pg.draw.circle(overlay, pg.Color('red'), center,
                           1, 2)

            self.image = overlay
            self.rect = overlay.get_rect(center=self.pointer_object.position)
        else:
            self.rect = self.image.get_rect(center=self.pointer_object.position)


pop = []
for _ in range(100):
    boid = Creature()
    boid.to_draw = ScreenObject(boid.movement, neutral_creature)
    pop.append(boid)

for _ in range(10):
    boid = Carnivore()
    boid.to_draw = ScreenObject(boid.movement, hostile_creature)
    pop.append(boid)