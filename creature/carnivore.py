from creature.creature import *
from res.const import *


class Carnivore(Creature):

    def __init__(self):
        super().__init__()
        self.type = CARNIVORE

        self.movement.perception = 1.2 * MAX_PERCEPTION

    def update(self, dt, boids) -> None:
        steering = pg.Vector2()

        if not Movement.can_wrap:
            steering += self.movement.avoid_edge()

        neighbors = self.movement.get_neighbors()

        if neighbors:
            separation = self.movement.separation(neighbors)
            alignment = self.movement.alignment(neighbors)
            cohesion = self.movement.cohesion(neighbors)
            hunt = self.movement.go_to(neighbors)
            # avoid = 3 * self.movement.avoid(neighbors)
            # DEBUG

            #separation *= -1
            # alignment *= 0
            # cohesion *= 0

            steering += separation + alignment + cohesion + hunt

        # steering = self.clamp_force(steering)
        self.movement.update(dt, steering)

        if (self.to_draw != None):
            self.to_draw.update()
