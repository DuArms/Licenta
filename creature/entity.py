import pygame as pg
from random import uniform
from creature.features.movement import Movement
from res.const import *


class Entity:
    debug = False

    def __init__(self, add_to_grid=True):
        self.is_ded = False
        self.to_draw = None

        self.eat_range = MAX_EAT_RANGE

        # Randomize starting position and velocity
        start_position = pg.math.Vector2(
            uniform(0.1 * Movement.max_x, 0.9 * Movement.max_x),
            uniform(0.1 * Movement.max_y, 0.9 * Movement.max_y))

        start_velocity = pg.math.Vector2(
            uniform(-1, 1) * Movement.max_speed,
            uniform(-1, 1) * Movement.max_speed)

        self.movement = Movement(
            position=start_position,
            velocity=start_velocity,
            min_speed=Movement.min_speed,
            max_speed=Movement.max_speed,
            max_force=Movement.max_force,
            parent=self,
            add_to_grid=add_to_grid)

        self.type = None

    def update(self, dt, entity, steering=None) -> None:
        if steering is None:
            steering = pg.Vector2()

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

    def select_closest_creature(self, entities: List['Entity']) -> 'Entity':
        min_dist = self.movement.perception
        target = None

        for f in entities:
            dist = f.movement.position.distance_to(self.movement.position)
            if dist < min_dist:
                min_dist = dist
                target = f

        return target
