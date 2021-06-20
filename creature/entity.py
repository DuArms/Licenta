import copy
from random import uniform

import pygame as pg

from algoritmi.Gene import *
from creature.features.movement import Movement


class Entity:
    debug = False
    MAX_AGE = 750
    def __init__(self, add_to_grid=True, generate_gene=True):
        self.is_ded = False
        self.score = 0

        self.to_draw = None
        self.type = None

        self.chance_to_be_seen = 1
        self.carnivores = []
        self.herbivores = []

        # Randomize starting position and velocity
        start_position = pg.math.Vector2(
            uniform(0.1 * Movement.max_x, 0.9 * Movement.max_x),
            uniform(0.1 * Movement.max_y, 0.9 * Movement.max_y))

        start_velocity = pg.math.Vector2(
            uniform(-1, 1) * Values.SPEED.high,
            uniform(-1, 1) * Values.SPEED.high)

        if generate_gene:
            self.genes: Dict[Gene] = dict()

            for gene in Values.ALL:
                self.genes[gene.id] = Gene(gene.low, gene.high)

            max_speed = self.genes[Values.SPEED.id].get_gene_value() * (
                    Values.SIZE.avg / self.genes[Values.SIZE.id].get_gene_value())

            self.movement = Movement(
                position=start_position,
                velocity=start_velocity,
                parent=self,
                add_to_grid=add_to_grid,
                max_speed=max_speed,
                max_force=self.genes[Values.FORCE.id].get_gene_value(),
                perception=self.genes[Values.PERCEPTION.id].get_gene_value(),
                field_of_view=self.genes[Values.FIELD_OF_VIEW.id].get_gene_value(),
                crowding=self.genes[Values.CROWDING.id].get_gene_value(),
            )

            self.eat_range = self.genes[Values.EAT_RANGE.id].get_gene_value()
            self.separation_importance = self.genes[Values.SEPARATION.id].get_gene_value()
            self.alignment_importance = self.genes[Values.ALIGNMENT.id].get_gene_value()
            self.cohesion_importance = self.genes[Values.COHESION.id].get_gene_value()
            self.avoid_importance = self.genes[Values.AVOID.id].get_gene_value()
            self.size = self.genes[Values.SIZE.id].get_gene_value()

            self.chance_to_be_seen = (self.size / Values.SIZE.avg) + 0.20
            self.focus = self.genes[Values.FOCUS.id].get_gene_value()
        else:
            self.movement = Movement(
                position=start_position,
                velocity=start_velocity,
                parent=self,
                add_to_grid=add_to_grid)

            self.eat_range = Values.EAT_RANGE.avg

            self.separation_importance = 1
            self.alignment_importance = 1
            self.cohesion_importance = 1
            self.avoid_importance = 1.2

            self.size = Values.SIZE.avg
            self.chance_to_be_seen = 1
            self.focus = 1

    def update(self, dt, entity, steering=None) -> None:
        if self.is_ded:
            return

        if steering is None:
            steering = pg.Vector2()

        neighbors = self.movement.get_neighbors()

        self.carnivores = []
        self.herbivores = []
        for x in neighbors:
            if x.type == EntityTypes.CARNIVORE:
                self.carnivores.append(x)
            elif x.type == EntityTypes.HERBIVORE:
                self.herbivores.append(x)

        if neighbors:
            separation = self.separation_importance * self.movement.separation(neighbors)
            alignment = self.movement.alignment(neighbors)
            cohesion = self.cohesion_importance * self.movement.cohesion(neighbors)
            avoid = self.avoid_importance * self.movement.avoid(self.carnivores)

            steering += separation + alignment + cohesion + avoid

        self.movement.update(dt, steering)

        if self.to_draw is not None:
            self.to_draw.update()

    def select_closest_creature(self, entities: List['Entity']) -> 'Entity':
        min_dist = self.movement.perception
        target = None

        for f in entities:
            dist = f.movement.position.distance_to(self.movement.position)
            if dist < min_dist and f.size < self.size:
                min_dist = dist
                target = f

        return target

    def update_genes(self, genes):
        self.genes = copy.deepcopy(genes)

        max_speed = min(self.genes[Values.SPEED.id].get_gene_value() * (
                Values.SIZE.avg / self.genes[Values.SIZE.id].get_gene_value()), Values.SPEED.high + 1)

        self.movement.set_gene_values(
            max_speed=max_speed,
            max_force=self.genes[Values.FORCE.id].get_gene_value(),
            perception=self.genes[Values.PERCEPTION.id].get_gene_value(),
            field_of_view=self.genes[Values.FIELD_OF_VIEW.id].get_gene_value(),
        )
        self.focus = self.genes[Values.FOCUS.id].get_gene_value()

        self.eat_range = self.genes[Values.EAT_RANGE.id].get_gene_value()
        self.separation_importance = self.genes[Values.SEPARATION.id].get_gene_value()
        self.alignment_importance = self.genes[Values.ALIGNMENT.id].get_gene_value()
        self.cohesion_importance = self.genes[Values.COHESION.id].get_gene_value()
        self.avoid_importance = self.genes[Values.AVOID.id].get_gene_value()
        self.size = self.genes[Values.SIZE.id].get_gene_value()

        self.chance_to_be_seen = (self.size / Values.SIZE.avg)

    def print_genes(self):
        s = f'''type = {self}
        max_speed = {self.movement.max_speed}
        max_force = {self.movement.max_force}
        
        perception = {self.movement.perception}
        field_of_view = {self.movement.field_of_view}  
        focus = {self.focus}  
        
        separation_importance = {self.separation_importance}
        alignment_importance = {self.alignment_importance}
        cohesion_importance = {self.cohesion_importance}
        avoid_importance = {self.avoid_importance}
        
        size = {self.size}'''

        print(s)
