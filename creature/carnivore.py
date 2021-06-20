from creature.entity import *
from res.const import *


class Carnivore(Entity):

    def __init__(self, add_to_grid=True, generate_gene=True):
        super().__init__(add_to_grid=add_to_grid, generate_gene=generate_gene)
        self.type = EntityTypes.CARNIVORE

        if not generate_gene:
            self.movement.perception = 1.2 * Values.PERCEPTION.high
            self.movement.max_speed = 1.0 * self.movement.max_speed

        self.moves_allowed = MOVES_ALLOWED

    def update(self, dt, entity: List[Entity], steering=None) -> None:
        if self.is_ded:
            return

        steering = pg.Vector2()

        neighbors = self.movement.get_neighbors()

        carnivores = []
        herbivores = []

        for x in neighbors:
            if x.type == EntityTypes.CARNIVORE:
                carnivores.append(x)
            elif x.type == EntityTypes.HERBIVORE:
                herbivores.append(x)

        self.neighbors = neighbors

        if neighbors:
            separation = self.separation_importance * self.movement.separation(carnivores)
            alignment = self.alignment_importance * self.movement.alignment(carnivores)
            cohesion = self.cohesion_importance * self.movement.cohesion(carnivores)
            avoid = self.avoid_importance * self.movement.avoid(carnivores)
            hunt = self.movement.go_to(herbivores)
            target = self.select_closest_creature(herbivores)

            if target is not None:
                hunt += self.movement.go_to([target])

            steering += separation + alignment + cohesion + hunt + avoid

        self.movement.update(dt, steering)

        c_mass = sum(map(lambda x: x.size, herbivores)) * 0.40 + self.size
        for food in filter(lambda x: x.movement.position.distance_to(self.movement.position) < self.eat_range,
                           herbivores):
            if food.size / c_mass < 0.40:
                Movement.hashmap.remove(food.movement, Movement.hashmap.key(food.movement))
                food.is_ded = True
                self.score += CARNIVORE_EAT_VALUE
                for carnivore in carnivores:
                    carnivore.score += CARNIVORE_EAT_VALUE * 0.10
            else:
                food.size -= self.size / food.size

                break

        for food in filter(lambda x: x.movement.position.distance_to(self.movement.position) < self.eat_range,
                           carnivores):
            if food.size / self.size < 0.15:
                Movement.hashmap.remove(food.movement, Movement.hashmap.key(food.movement))
                food.is_ded = True
                self.score += CARNIVORE_EAT_VALUE * 3

        if self.to_draw is not None:
            self.to_draw.update()
