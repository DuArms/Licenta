from __future__ import annotations
from typing import *
from pygame import Vector2
from enum import Enum

import numpy as np
import copy
from res.gui_const import *

np.random.seed(0)


class EntityTypes(Enum):
    CARNIVORE: Final = 0xA
    HERBIVORE: Final = 0xB
    PLANT: Final = 0xC


MAX_EAT_RANGE: Final = 20
MAX_PERCEPTION: Final = 60
