import pygame.image

from creature.carnivore import *
from creature.herbivore import *

size = 30

fish = pygame.image.load(cwd + '\\res\herbivore.png')
fish = pygame.transform.scale(fish, (size, size))
fish = pygame.transform.flip(fish, True, False)
neutral_creature = fish

# neutral_creature = pg.Surface((size, size), pg.SRCALPHA)
# pg.draw.polygon(neutral_creature, pg.Color('blue'),
#                 [(0, size * 0.25), (0, size * 0.75), (size, size / 2)])

fish = pygame.image.load(cwd + '\\res\carnivore.png')
fish = pygame.transform.scale(fish, (size, size))
fish = pygame.transform.flip(fish, True, False)
hostile_creature = fish

# hostile_creature = pg.Surface((size, size), pg.SRCALPHA)
# pg.draw.polygon(hostile_creature, pg.Color('red'),
#                 [(0, size * 0.25), (0, size * 0.75), (size, size / 2)])


plant_img = pg.Surface((size, size), pg.SRCALPHA)
pg.draw.circle(plant_img, pg.Color('PURPLE '),
               (size / 2, size / 2), size / 10)

population = []

plants = []

Movement.set_boundary(Movement.edge_distance_pct, MAP_WIDTH, MAP_HIGHT)


class ScreenObject(pg.sprite.Sprite):
    debug = False

    def __init__(self, object: Movement, image):
        super().__init__()
        self.original_image = image
        self.original_image_flipped = pygame.transform.flip(self.original_image, False, True)
        self.pointer_object = object
        self.image = image
        self.rect = self.image.get_rect(center=self.pointer_object.position)

        pass

    def update(self) -> None:
        if abs(self.pointer_object.heading) <= 90:
            self.image = pg.transform.rotate(self.original_image, -self.pointer_object.heading)
        else:
            self.image = pg.transform.rotate(
                self.original_image_flipped
                , -self.pointer_object.heading)

        self.rect = self.image.get_rect(center=self.pointer_object.position)

        if ScreenObject.debug:
            center = pg.Vector2((self.pointer_object.perception, self.pointer_object.perception))

            velocity = pg.Vector2(self.pointer_object.velocity)
            velocity += center

            acceleration = pg.Vector2(self.pointer_object.acceleration)
            acceleration += center

            steering = pg.Vector2(self.pointer_object.steering)
            steering += center

            overlay = pg.Surface((self.pointer_object.perception * 2, self.pointer_object.perception * 2), pg.SRCALPHA)

            overlay.blit(self.image, self.image.get_rect(center=center))
            pg.draw.circle(overlay, pg.Color('green'), center,
                           self.pointer_object.perception, 2)
            # draw field of view lines
            _, angle = self.pointer_object.velocity.as_polar()

            sight = copy.deepcopy(self.pointer_object.velocity)
            sight.from_polar((self.pointer_object.perception, angle - self.pointer_object.field_of_view))
            sight += center
            pg.draw.line(overlay, pg.Color('pink'), center, sight, 1)

            sight = copy.deepcopy(self.pointer_object.velocity)
            sight.from_polar((self.pointer_object.perception, angle + self.pointer_object.field_of_view))
            sight += center
            pg.draw.line(overlay, pg.Color('pink'), center, sight, 1)

            tenp_vector = Vector2()
            tenp_vector.from_polar((self.pointer_object.perception, angle))
            tenp_vector += center

            pg.draw.line(overlay, pg.Color('orange'), center,
                         tenp_vector, 3)

            pg.draw.line(overlay, pg.Color('green'), center, velocity, 3)

            pg.draw.line(overlay, pg.Color('red'), center,
                         acceleration, 3)

            pg.draw.line(overlay, pg.Color('blue'), center,
                         steering, 3)

            pg.draw.circle(overlay, pg.Color('red'), center,
                           1, 2)

            self.image = overlay
            self.rect = overlay.get_rect(center=self.pointer_object.position)
        else:
            self.rect = self.image.get_rect(center=self.pointer_object.position)


# for _ in range(50):
#     entity = Herbivore(generate_gene=False)
#     entity.to_draw = ScreenObject(entity.movement, neutral_creature)
#     population.append(entity)

# for _ in range(5):
#     entity = Carnivore(generate_gene=False)
#     entity.to_draw = ScreenObject(entity.movement, hostile_creature)
#     population.append(entity)

for _ in range(2000):
    entity = Plant()
    entity.to_draw = ScreenObject(entity.movement, plant_img)
    plants.append(entity)

import pickle

car = pickle.load(open("D:\Facultate\TrueLicenta\int_DATA\\r3\carnivores.data", "rb"))
her = pickle.load(open("D:\Facultate\TrueLicenta\int_DATA\\r3\\herbivores.data", "rb"))

Movement.set_boundary(Movement.edge_distance_pct, MAP_WIDTH, MAP_HIGHT)

herbivores = pickle.loads(her[-1])
carnivores = pickle.loads(car[-1])

car = sorted(carnivores, key=lambda x : -x.score)
her = sorted(herbivores, key=lambda x : -x.score)

for h in her[:200]:
    entity: Entity = h
    entity.is_ded = False
    entity.movement.max_speed = min(entity.movement.max_speed, Values.SPEED.high * 0.75)
    entity.movement.random_pos()
    entity.to_draw = ScreenObject(entity.movement, neutral_creature)
    population.append(entity)

#print(car[0].print_genes())

for c in car[:5]:
    entity: Entity = c
    entity.is_ded = False
    entity.movement.max_speed = min(entity.movement.max_speed, Values.SPEED.high * 0.75 )
    entity.movement.random_pos()

    entity.to_draw = ScreenObject(entity.movement, hostile_creature)
    population.append(entity)

