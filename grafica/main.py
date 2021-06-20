import pygame

from res.const import *
from grafica.screen_object import *
from creature.entity import Entity

pg = pygame
fps = 60.0
plants_count = 50

# Set up the drawing window
class GUI:
    debug = False

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([GAME_WIDTH, GAME_HIGHT])

        self.map_x = int(GAME_WIDTH * 0.10)
        self.map_y = int(GAME_HIGHT * 0.10)

        self.world_coord = (self.map_x, self.map_y)
        self.world = pygame.Surface((MAP_WIDTH, MAP_HIGHT))

        self.dt = 0.5

        self.grid = pygame.Surface((MAP_WIDTH, MAP_HIGHT), pygame.SRCALPHA)
        for i in range(0, MAP_HIGHT, Values.PERCEPTION.high):
            a = (0, i)
            b = (MAP_WIDTH, i)
            pg.draw.line(self.grid, pg.Color('green'), a, b, 1)

        for j in range(0, MAP_WIDTH, Values.PERCEPTION.high):
            a = (j, 0)
            b = (j, MAP_HIGHT)
            pg.draw.line(self.grid, pg.Color('green'), a, b, 1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            game_gui.draw()
            #print(self.clock.tick(fps))
            self.clock.tick(fps)
            self.tick()

    def draw(self):

        self.screen.fill(WHITE)
        self.world.fill(WHITE)

        self.draw_frame()

        if GUI.debug:
            self.debugf()

        self.screen.blit(self.world, self.world_coord)
        pygame.display.flip()

    def tick(self):
        global population, plants

        new_population = [x for x in population if not x.is_ded]
        new_plants = [x for x in plants if not x.is_ded]

        population = new_population
        plants = new_plants

        # print(len(population))

        for creature in population:
            creature.update(self.dt, population)

        if len(plants) < plants_count:
            for x in range(plants_count - len(plants)):
                entity = Plant()
                entity.to_draw = ScreenObject(entity.movement, plant_img)
                plants.append(entity)

    def draw_frame(self):
        for plant in plants:
            img: ScreenObject = plant.to_draw
            self.world.blit(img.image, img.rect)

        for creature in population:
            img: ScreenObject = creature.to_draw

            self.world.blit(img.image, img.rect)

    def debugf(self):
        self.world.blit(self.grid, self.grid.get_rect())

        pass


game_gui = GUI()

if __name__ == "__main__":
    game_gui.run()
