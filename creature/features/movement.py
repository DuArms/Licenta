import pygame as pg

from res.const import *

from Algoritmi.SpatialHash import *


class Movement(pg.sprite.Sprite):
    can_wrap = False
    debug = False
    max_x = 0
    max_y = 0

    min_speed = 0
    max_speed = 2
    max_force = 3
    max_turn = 30
    perception = MAX_PERCEPTION
    crowding = 15

    field_of_view = 120

    edge_distance_pct = 5
    edges = [0, 0, 0, 0]

    hashmap: SpatialHash = None

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
                 max_force, can_wrap, parent):

        super().__init__()

        # set limits
        self.parent = parent
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.max_force = max_force

        self.position = pg.Vector2(position)
        self.acceleration = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(velocity)

        Movement.hashmap.insert(self)
        self.steering = pg.Vector2([0, 0])

        self.heading = 0.0

    def update(self, dt, steering):
        old_grid_key = self.hashmap.key(self)

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

        # update grid
        if Movement.hashmap.key(self) != old_grid_key:
            Movement.hashmap.remove(self, old_grid_key)
            Movement.hashmap.insert(self)

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

    def avoid(self, creatures: 'Creature') -> pg.Vector2:
        steering = pg.Vector2()

        for creature in creatures:
            if creature.type == CARNIVORE:
                movement_info: Movement = creature.movement

                steering -= movement_info.position - self.position

        steering = self.clamp_force(steering)

        return steering

    def go_to(self, creatures: 'Creature') -> pg.Vector2:
        steering = pg.Vector2()

        for creature in creatures:
            if creature.type != CARNIVORE:
                movement_info: Movement = creature.movement

                steering += movement_info.position - self.position

        steering = self.clamp_force(steering)

        return steering

    def get_neighbors(self) -> List['Creature']:

        my_key = Movement.hashmap.key(self)

        neighbors = [ Movement.hashmap.query_by_key(my_key)]
        for i in range(-1, 2):
            for j in range(-1, 2):
                n_key = Movement.hashmap.key_from_coord(self.position - (self.perception * i, self.perception * j))
                if my_key != n_key:
                    res = Movement.hashmap.query_by_key(n_key)
                    neighbors.append(res)

        # neighbors = Movement.hashmap.query(self)
        # creatures = [ x.parent for x in neighbors]
        creatures = []
        for s in neighbors:
            l = [x.parent for x in s]
            creatures.extend(l)

        neighbors = []

        for creature in creatures:
            if creature != self:

                dist = self.position.distance_to(creature.movement.position)

                angle = self.position.angle_to(creature.movement.position)

                _, curent_angle = self.velocity.as_polar()

                if abs(angle) < abs(curent_angle) + Movement.field_of_view:

                    if dist < self.perception and abs(angle) <= self.field_of_view:
                        neighbors.append(creature)

        return neighbors


Movement.set_boundary(Movement.edge_distance_pct)
Movement.hashmap = hashmap = SpatialHash(MAX_PERCEPTION * 2)
