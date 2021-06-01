import pygame as pg

from res.const import *


class Movement(pg.sprite.Sprite):
    # default image is a li'l white triangle
    image = pg.Surface((10, 10), pg.SRCALPHA)
    pg.draw.polygon(image, pg.Color('white'),
                    [(15, 5), (0, 2), (0, 8)])

    can_wrap = False
    debug = False
    max_x = 0
    max_y = 0

    min_speed = .01
    max_speed = .2
    max_force = 1
    max_turn = 5
    perception = 60
    crowding = 15

    edge_distance_pct = 5
    edges = [0, 0, 0, 0]

    @staticmethod
    def set_boundary(edge_distance_pct):
        Movement.max_x = MAP_WIDTH
        Movement.max_y = MAP_HIGHT

        margin_w = Movement.max_x * edge_distance_pct / 100
        margin_h = Movement.max_y * edge_distance_pct / 100

        Movement.edges = [margin_w,
                          margin_h,
                          Movement.max_x - margin_w,
                          Movement.max_y - margin_h]

    def __init__(self, position, velocity, min_speed, max_speed,
                 max_force, can_wrap):

        super().__init__()

        # set limits
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.max_force = max_force

        self.position = pg.Vector2(position)
        self.acceleration = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(velocity)

        self.steering = pg.Vector2([0, 0])

        self.heading = 0.0

    def update(self, dt, steering):
        self.steering = steering

        self.acceleration = steering * dt

        # enforce turn limit
        _, old_heading = self.velocity.as_polar()
        new_velocity = self.velocity + self.acceleration * dt
        speed, new_heading = new_velocity.as_polar()

        heading_diff = 180 - (180 - new_heading + old_heading) % 360
        if abs(heading_diff) > self.max_turn:
            if heading_diff > self.max_turn:
                new_heading = old_heading + self.max_turn
            else:
                new_heading = old_heading - self.max_turn

        self.velocity.from_polar((speed, new_heading))

        # enforce speed limit
        speed, self.heading = self.velocity.as_polar()

        if speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)

        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # move
        self.position += self.velocity * dt

        if self.can_wrap:
            self.wrap()
        else:
            self.contain()

    def avoid_edge(self):
        left = self.edges[0] - self.position.x
        up = self.edges[1] - self.position.y
        right = self.position.x - self.edges[2]
        down = self.position.y - self.edges[3]

        scale = max(left, up, right, down)

        if scale > 0:
            center = (Movement.max_x / 2, Movement.max_y / 2)
            steering = pg.Vector2(center)
            steering -= self.position
        else:
            steering = pg.Vector2()

        return steering

    def wrap(self):
        if self.position.x < 0:
            self.position.x += Movement.max_x
        elif self.position.x > Movement.max_x:
            self.position.x -= Movement.max_x

        if self.position.y < 0:
            self.position.y += Movement.max_y
        elif self.position.y > Movement.max_y:
            self.position.y -= Movement.max_y

    def contain(self):
        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x > Movement.max_x:
            self.position.x = Movement.max_x

        if self.position.y < 0:
            self.position.y = 0
        elif self.position.y > Movement.max_y:
            self.position.y = Movement.max_y

    def clamp_force(self, force):
        if 0 < force.magnitude() > self.max_force:
            force.scale_to_length(self.max_force)

        return force

    def separation(self, creatures: 'Creature') -> pg.Vector2:
        steering = pg.Vector2()
        for creature in creatures:
            movement_info: Movement = creature.movement
            dist = self.position.distance_to(movement_info.position)

            if dist < self.crowding:
                steering -= movement_info.position - self.position
        steering = self.clamp_force(steering)
        return steering

    def alignment(self, creatures: 'Creature') -> pg.Vector2:
        steering = pg.Vector2()
        for creature in creatures:
            movement_info: Movement = creature.movement
            steering += movement_info.velocity

        steering /= len(creatures)
        steering -= self.velocity
        steering = self.clamp_force(steering)
        return steering / 8

    def cohesion(self, creatures: 'Creature') -> pg.Vector2:
        steering = pg.Vector2()
        for creature in creatures:
            movement_info: Movement = creature.movement

            steering += movement_info.position
        steering /= len(creatures)
        steering -= self.position
        steering = self.clamp_force(steering)
        return steering / 100

    def get_neighbors(self, boids: 'Creature') -> List['Creature']:
        neighbors = []
        for boid in boids:
            if boid != self:
                dist = self.position.distance_to(boid.movement.position)
                if dist < self.perception:
                    neighbors.append(boid)
        return neighbors
