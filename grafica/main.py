import pygame

from res.const import *
from grafica.transform import *
from creature.creature import Creature

pg = pygame


# Set up the drawing window
class GUI:
    debug = True

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([GAME_WIDTH, GAME_HIGHT])

        self.map_x = int(GAME_WIDTH * 0.10)
        self.map_y = int(GAME_HIGHT * 0.10)

        self.world_coord = (self.map_x, self.map_y)
        self.world = pygame.Surface((MAP_WIDTH, MAP_HIGHT))

        self.dt = 1

        self.grid = pygame.Surface((MAP_WIDTH, MAP_HIGHT),pygame.SRCALPHA)
        for i in range(0, MAP_HIGHT, MAX_PERCEPTION):
            a = (0, i)
            b = (MAP_WIDTH, i)
            pg.draw.line(self.grid, pg.Color('green'), a, b, 1)

        for j in range(0, MAP_WIDTH, MAX_PERCEPTION):
            a = (j, 0)
            b = (j, MAP_HIGHT)
            pg.draw.line(self.grid, pg.Color('green'), a, b, 1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            game_gui.draw()

            # for pop in popoluation:
            #     pop.tick()

        #  tick()

    def draw(self):

        self.screen.fill(WHITE)
        self.world.fill(WHITE)

        self.draw_frame()

        if GUI.debug:
            self.debugf()

        self.screen.blit(self.world, self.world_coord)
        pygame.display.flip()

        self. tick()
        from time import sleep
        #  print(Movement.hashmap)
        # sleep(10)

    def tick(self):
        for creature in pop:
            creature.update(self.dt, pop)

    def draw_frame(self):
        for creature in pop:
            img: ScreenObject = creature.to_draw

            self.world.blit(img.image, img.rect)



    def debugf(self):
        self.world.blit( self.grid , self.grid.get_rect())


game_gui = GUI()

if __name__ == "__main__":
    game_gui.run()
