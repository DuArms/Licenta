import pygame as pg
from pygame.math import Vector2

from algoritmi.SpatialHash import *
from res.gui_const import *
from random import uniform
import numpy as np


class Movement(pg.sprite.Sprite):
    can_wrap = True
    debug = False
    max_x = 0
    max_y = 0

    max_turn = Values.TURN.high
    crowding = Values.CROWDING.avg

    field_of_view = Values.FIELD_OF_VIEW.high

    edge_distance_pct = 5
    edges = [0, 0, 0, 0]

    hashmap: SpatialHash = None

    @staticmethod
    def set_boundary(edge_distance_pct, x, y):
        Movement.max_x = x
        Movement.max_y = y

        margin_w = Movement.max_x * edge_distance_pct / 100
        margin_h = Movement.max_y * edge_distance_pct / 100

        Movement.edges = [margin_w,
                          margin_h,
                          Movement.max_x - margin_w,
                          Movement.max_y - margin_h]

    def __init__(self,
                 position,
                 velocity,
                 parent=None,
                 add_to_grid=True,

                 max_speed=Values.SPEED.high,
                 max_force=Values.FORCE.high,
                 perception=Values.PERCEPTION.high,
                 field_of_view=Values.FIELD_OF_VIEW.high,
                 crowding=Values.CROWDING.high,

                 ):

        super().__init__()

        # set limits

        self.parent = parent
        self.position: Vector2 = Vector2(position)
        self.acceleration: Vector2 = Vector2(0, 0)
        self.velocity: Vector2 = Vector2(velocity)

        self.coord = np.asarray((self.position[0], self.position[1]))

        self.min_speed = Values.SPEED.low

        self.max_speed = max_speed
        self.max_force = max_force

        self.perception = perception
        self.field_of_view = field_of_view

        self.crowding = crowding

        if add_to_grid:
            Movement.hashmap.insert(self)

        self.steering: Vector2 = Vector2([0, 0])
        self.heading = 0.0

    def set_gene_values(self, max_speed=Values.SPEED.high,
                        max_force=Values.FORCE.high,
                        perception=Values.PERCEPTION.high,
                        field_of_view=Values.FIELD_OF_VIEW.high, ):

        self.max_speed = max_speed
        self.max_force = max_force

        self.perception = perception
        self.field_of_view = field_of_view

    def random_pos(self):
        self.position = pg.math.Vector2(
            uniform(0.1 * Movement.max_x, 0.9 * Movement.max_x),
            uniform(0.1 * Movement.max_y, 0.9 * Movement.max_y))


    def update(self, dt, steering):
        old_grid_key = self.hashmap.key(self)

        if not Movement.can_wrap:
            steering += self.avoid_edge()

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

        self.coord = np.asarray((self.position[0], self.position[1]))

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

    def separation(self, entities: 'Entity') -> pg.Vector2:
        steering = pg.Vector2()

        for entity in entities:
            movement_info: Movement = entity.movement
            dist = self.position.distance_to(movement_info.position)

            if dist < self.crowding:
                steering -= movement_info.position - self.position
        steering = self.clamp_force(steering)
        return steering

    def alignment(self, entities: 'Entity') -> pg.Vector2:
        if not entities:
            return Vector2()

        steering = pg.Vector2()
        for entity in entities:
            movement_info: Movement = entity.movement
            steering += movement_info.velocity

        steering /= len(entities)
        steering -= self.velocity
        steering = self.clamp_force(steering)
        return steering / 4

    def cohesion(self, entities: 'Entity') -> pg.Vector2:
        if not entities:
            return Vector2()

        steering = pg.Vector2()
        for entity in entities:
            movement_info: Movement = entity.movement

            steering += movement_info.position
        steering /= len(entities)
        steering -= self.position
        steering = self.clamp_force(steering)
        return steering / 100

    def avoid(self, entities: 'Entity') -> pg.Vector2:
        steering = pg.Vector2()

        for entity in entities:
            if entity.type == EntityTypes.CARNIVORE:
                movement_info: Movement = entity.movement
                dist = movement_info.position.distance_to(self.position)
                steering -= (self.perception * 1.1 - dist) * (movement_info.position - self.position)

        steering = self.clamp_force(steering)

        return steering

    def go_to(self, entities: 'Entity') -> pg.Vector2:
        steering = pg.Vector2()

        for entity in entities:
            movement_info: Movement = entity.movement
            dist = movement_info.position.distance_to(self.position)
            steering += (self.perception * 1.1 - dist) * (movement_info.position - self.position)

        steering = self.clamp_force(steering)

        return steering

    def get_neighbors(self) -> List['Entity']:
        my_key = Movement.hashmap.key(self)

        neighbors = [Movement.hashmap.query_by_key(my_key)]
        for i in range(-1, 2):
            for j in range(-1, 2):
                n_key = Movement.hashmap.key_from_coord(self.position - (self.perception * i, self.perception * j))
                if my_key != n_key:
                    res = Movement.hashmap.query_by_key(n_key)
                    neighbors.append(res)

        # neighbors = Movement.hashmap.query(self)
        # entities = [ x.parent for x in neighbors]
        entities = []
        for s in neighbors:
            l = [x.parent for x in s]
            entities.extend(l)

        neighbors = []

        for entity in entities:
            if entity != self:
                dist = self.position.distance_to(entity.movement.position)
                if dist < self.perception:
                    angle = self.velocity.angle_to(entity.movement.position - self.position)
                    angle = angle % 180

                    if angle < Movement.field_of_view:
                        sc = 0.2
                        if angle < 0.30 * self.field_of_view:
                            sc += 0.5
                        sc += entity.chance_to_be_seen + self.parent.focus

                        if np.random.rand() < sc:
                            neighbors.append(entity)

        return neighbors


Movement.set_boundary(Movement.edge_distance_pct, MAP_WIDTH, MAP_HIGHT)
Movement.hashmap = hashmap = SpatialHash(Values.PERCEPTION.high * 2)
