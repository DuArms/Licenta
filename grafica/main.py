import pygame

from res.const import *
from grafica.transform import *
from creature.creature import Creature

pg = pygame


# Set up the drawing window
class GUI:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([GAME_WIDTH, GAME_HIGHT])

        self.map_x = int(GAME_WIDTH * 0.10)
        self.map_y = int(GAME_HIGHT * 0.10)

        self.world_coord = (self.map_x, self.map_y)
        self.world = pygame.Surface((MAP_WIDTH,MAP_HIGHT))

        self.dt = 0.1

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

        self.screen.blit(self.world, self.world_coord)
        pygame.display.flip()

        self.dt = 10  #self.clock.tick(60)

    def draw_frame(self):
        for creature in pop:
            img: ScreenObject = creature.to_draw

            self.world.blit(img.image, img.rect)

            creature.update(self.dt, pop)


game_gui = GUI()

if __name__ == "__main__":
    game_gui.run()
