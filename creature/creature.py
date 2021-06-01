import pygame as pg
from random import uniform
from creature.features.movement import Movement

Movement.set_boundary(Movement.edge_distance_pct)


class Creature:
    # CONFIG
    debug = False

    ###############

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
            Movement.can_wrap)

    def update(self, dt, boids) -> None:
        steering = pg.Vector2()

        if not Movement.can_wrap:
            steering += self.movement.avoid_edge()

        neighbors = self.movement.get_neighbors(boids)

        if neighbors:
            separation = self.movement.separation(neighbors)
            alignment = self.movement.alignment(neighbors)
            cohesion = self.movement.cohesion(neighbors)

            # DEBUG
            # separation *= 0
            # alignment *= 0
            # cohesion *= 0

            steering += separation + alignment + cohesion

        # steering = self.clamp_force(steering)
        self.movement.update(dt, steering)

        if ( self.to_draw != None):
            self.to_draw.update()

        if self.movement.position[0] < 0 :
            print(self.movement.position)
