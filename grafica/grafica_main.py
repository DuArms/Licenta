import pygame

from creatures.creature import *
from world.test import *

zergling = pygame.image.load("../resurse/zergling.png")
zergling = pygame.transform.scale(zergling, (80, 50))

zergling_2 = pygame.transform.flip(zergling, True, False)


# Set up the drawing window
class GUI:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([GAME_WIDTH, GAME_HIGHT])

        self.map_x = int(GAME_WIDTH * 0.10)
        self.map_y = int(GAME_HIGHT * 0.10)
        self.scale_x = int(GAME_WIDTH * 0.80)
        self.scale_y = int(GAME_HIGHT * 0.80)

        self.world_coord = (self.map_x, self.map_y)
        self.world = pygame.Surface((self.scale_x, self.scale_y))

        self.individ_size = min(self.scale_x * 0.04, self.scale_y * 0.04)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            game_gui.draw()

            # for pop in popoluation:
            #     pop.tick()

            tick()

    def draw(self):

        self.screen.fill(WHITE)
        self.world.fill(WHITE)

        self.draw_frame()

        self.screen.blit(self.world, self.world_coord)
        pygame.display.flip()

        self.clock.tick(60)

    def align_to_frame(self, pos):
        x, y = pos

        x = x / MAP_SIZE
        y = y / MAP_SIZE

        x = x * self.scale_x
        y = y * self.scale_y

        return x, y

    def draw_frame(self):

        for vizion_circle, direction_momentum in to_draw():
            vizion_circle[0] = self.align_to_frame(vizion_circle[0])
            direction_momentum[0] = self.align_to_frame(direction_momentum[0])
            direction_momentum[1] = self.align_to_frame(direction_momentum[1])

            pygame.draw.circle(self.world, GREEN, vizion_circle[0], vizion_circle[1], 2)
            pygame.draw.line(self.world, RED, direction_momentum[0], direction_momentum[1], 4)

        info = [
            (self.align_to_frame(pop.get_coord()), RED if pop.food else BLUE) for pop in populations
        ]

        # info.sort(key=lambda x: x[1] == RED)
        i = 0
        for pos, col in info:
            if col == BLUE:
                img = None
                if populations[i].movement.momentum[0] > 0:
                    img = zergling
                else:
                    img = zergling_2

                rect = img.get_rect()
                rect.center = pos
                self.world.blit(img, rect)

        for food in food_supply:
            pos = self.align_to_frame(food.get_coord())
            pygame.draw.circle(self.world, ORENGE, pos, self.individ_size)


game_gui = GUI()

if __name__ == "__main__":
    game_gui.run()
