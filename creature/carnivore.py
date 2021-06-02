from creature.entity import *
from res.const import *


class Carnivore(Entity):

    def __init__(self):
        super().__init__()
        self.type = EntityTypes.CARNIVORE

        self.movement.perception = 1.2 * MAX_PERCEPTION
        self.movement.max_speed = 1.0 * self.movement.max_speed
        self.movement.field_of_view = 60

    def update(self, dt, entity: List[Entity], steering=None) -> None:
        steering = pg.Vector2()

        neighbors = self.movement.get_neighbors()

        carnivores = []
        herbivores = []

        for x in neighbors:
            if x.type == EntityTypes.CARNIVORE:
                carnivores.append(x)
            elif x.type == EntityTypes.HERBIVORE:
                herbivores.append(x)

        if neighbors:
            separation = self.movement.separation(carnivores)
            alignment = self.movement.alignment(carnivores)
            cohesion = self.movement.cohesion(carnivores)

            hunt = self.movement.go_to(herbivores)
            target = self.select_closest_creature(herbivores)

            if target is not None:
                hunt += self.movement.go_to([target])

            steering += separation + alignment + cohesion + hunt

        self.movement.update(dt, steering)

        for food in herbivores:
            if food.movement.position.distance_to(self.movement.position) < self.eat_range:
                Movement.hashmap.remove(food.movement, Movement.hashmap.key(food.movement))

                food.is_ded = True

        if self.to_draw is not None:
            self.to_draw.update()
