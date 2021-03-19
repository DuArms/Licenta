from creatures.creature import *


class Food(Creature):

    def __init__(self):
        super().__init__()
        self.food = True


food_supply: Set[Food] = {
    Food() for _ in range(MAX_FOOD)
}
