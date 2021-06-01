from __future__ import annotations
from typing  import *

import numpy as np
import copy
from res.gui_const import *

np.random.seed(0)

CARNIVORE = 1
HERBIVORE = 2


MAP_SIZE = 600
MAP_RANGE = 100

R = 30

# Matematice
PI = np.math.pi



MAX_SPEED = 10

MAX_PERCEPTION = 60

MIN_SPEED = 5

MAX_FOOD = 1
# Constante de debug

SOMN = 15



ZONE_ADIACENTE = []
for curent_viz_range in range(1, 10):
    lista = []
    for i in range(-curent_viz_range, curent_viz_range + 1):
        for j in range(-curent_viz_range, curent_viz_range + 1):
            if abs(i) == curent_viz_range or abs(j) == curent_viz_range:
                lista.append((i, j))
    ZONE_ADIACENTE.append(lista)
