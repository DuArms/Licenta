import random
import time
import math
from functools import cache
from typing import List

from res.const import *


class SpatialHash(object):
    def dict_setdefault(self, k, d=None) -> set:
        if d is None:
            d = set()

        r = self.grid.get(k, d)
        if k not in self.grid:
            self.grid[k] = d
        return r

    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}

    def key(self, obj):
        point = obj.position
        return self.key_from_coord(point)

    def key_from_coord(self, point):
        cell_size = self.cell_size
        return (
            int((math.floor(point[0] / cell_size)) * cell_size),
            int((math.floor(point[1] / cell_size)) * cell_size)
        )

    def insert(self, obj):
        self.dict_setdefault(self.key(obj)).add(obj)

    def remove(self, obj, key):

        self.dict_setdefault(key).remove(obj)

    @cache
    def query(self, obj):
        return self.dict_setdefault(self.key(obj))

    @cache
    def query_by_key(self, key):
        return self.dict_setdefault(key)

    def __repr__(self):
        s = ""

        for k, el in self.grid.items():
            s += str(k) + "->" + str(el) + '\n'

        return s
