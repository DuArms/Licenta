import math
from collections import defaultdict

from res.const import *


class SpatialHash(object):

    def __init__(self, cell_size=Values.PERCEPTION.high * 2):
        self.cell_size = cell_size
        self.grid = defaultdict(set)

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
        self.grid[self.key(obj)] |= {obj}

    def remove(self, obj, key):
        d = self.grid[key]
        if obj in d:
            d.remove(obj)

    def query(self, obj):
        return self.grid[self.key(obj)]

    def query_by_key(self, key):
        if key in self.grid:
            return self.grid[key]
        else:
            return set()

    def __repr__(self):
        s = ""
        a = 0
        for k, el in self.grid.items():
            a += len(el)
        # s += str(k) + "->" + str(el) + '\n'

        return s + str(a)
