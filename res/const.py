from __future__ import annotations

import os
from enum import Enum
from typing import *
from pygame import Vector2
import numpy as np

cwd = os.getcwd()
cwd = cwd.rsplit('\\', 1)[0]


# np.random.seed(0)


class EntityTypes(Enum):
    CARNIVORE: Final = 0xA
    HERBIVORE: Final = 0xB
    PLANT: Final = 0xC


class Values:
    class Stat:
        def __init__(self, low, high, ID):
            self.low: int = low
            self.avg = (low + high) // 2
            self.high: int = high
            self.id: int = ID

    EAT_RANGE: Final = Stat(10, 15, 0)
    PERCEPTION: Final = Stat(45, 60, 1)
    FOCUS: Final = Stat(0, 2, 13)
    FIELD_OF_VIEW: Final = Stat(30, 170, 7)

    SPEED: Final = Stat(1, 10, 3)
    FORCE: Final = Stat(1, 3, 4)
    TURN: Final = Stat(15, 35, 5)
    CROWDING: Final = Stat(10, 20, 6)

    SEPARATION = Stat(0, 1.5, 8)
    ALIGNMENT = Stat(0, 1.5, 9)
    COHESION = Stat(0, 1.5, 10)
    AVOID = Stat(0, 2, 11)

    SIZE: Final = Stat(1, 300, 12)

    ALL: set[Stat] = {EAT_RANGE, PERCEPTION, SPEED, FORCE, TURN, CROWDING, FIELD_OF_VIEW,
                      SEPARATION, ALIGNMENT, COHESION, AVOID, SIZE, FOCUS
                      }

    NUMBER_OF_GENES: Final = len(ALL)

    cost = 10


MIN_SCORE_VALUE = 500
CARNIVORE_EAT_VALUE = 100
HERBIVORE_EAT_VALUE = 50

MOVES_ALLOWED = 150

values_dict = dict()
for x in Values.ALL:
    values_dict[x.id] = x
