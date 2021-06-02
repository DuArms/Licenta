import pygame as pg
from random import uniform
from creature.features.movement import Movement
from res.const import *



class Creature:
    debug = False

    def __init__(self):
        self.to_draw = None
        # Randomize starting position and velocity
        start_position = pg.math.Vector2(
            uniform(0, Movement.max_x),
            uniform(0, Movement.max_y))

        start_velocity = pg.math.Vector2(
            uniform(-1, 1) * Movement.max_speed,
            uniform(-1, 1) * Movement.max_speed)

        self.movement = Movement(
            start_position,
            start_velocity,
            Movement.min_speed,
            Movement.max_speed,
            Movement.max_force,
            Movement.can_wrap,
            self)

        self.type = None

    def update(self, dt, boids) -> None:
        steering = pg.Vector2()

        if not Movement.can_wrap:
            steering += self.movement.avoid_edge()

        neighbors = self.movement.get_neighbors()

        if neighbors:
            separation = self.movement.separation(neighbors)
            alignment = self.movement.alignment(neighbors)
            cohesion = self.movement.cohesion(neighbors)
            avoid = 1.2 * self.movement.avoid(neighbors)

            steering += separation + alignment + cohesion + avoid

        self.movement.update(dt, steering)

        if self.to_draw is not None:
            self.to_draw.update()
