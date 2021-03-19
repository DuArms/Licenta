import numpy as np
import copy
from resurse.GUI_const import *


np.random.seed(0)




MAP_SIZE = 600
MAP_RANGE = 100

R = 30

# Matematice
PI = np.math.pi

# Infectie
INFECTION_CHANCE = 0.1
MAX_SPEED = 10
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
