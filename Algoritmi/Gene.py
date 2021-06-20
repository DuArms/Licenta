import math

import numpy as np

from res.const import *


def my_bin(x) -> str:
    return f'{x:0{32}b}'


class Gene:
    debug = False

    def __init__(self, min_value, max_value, size=31, gene=None):

        if size > 31:
            size = 31

        self.size = size
        self.max_value = max_value
        self.min_value = min_value

        self.cap = (1 << size) - 1

        if gene is not None:
            self.gene: int = gene
        else:
            self.gene = np.random.randint(0, 1 << size)

    def get_gene_proc(self):
        return self.gene / self.cap

    def get_gene_value(self):
        ret = (self.gene / self.cap) * (self.max_value - self.min_value)
        ret += self.min_value

        return ret

    def mutation(self):
        x = np.random.randint(0, self.cap + 1)
        self.gene = self.gene ^ x


    def cross(self, other_gene: 'Gene'):
        cut_points = np.random.randint(0, self.size, 2)
        cut_points.sort(0)

        cut = ((1 << cut_points[1]) - 1) ^ ((1 << cut_points[0]) - 1)

        gene_a = self.gene & cut
        gene_b = other_gene.gene & cut

        kid1 = (self.gene & ~cut) | gene_b
        kid2 = (other_gene.gene & ~cut) | gene_a

        if Gene.debug:
            print(cut_points)
            print(my_bin(self.gene))
            print(my_bin(other_gene.gene))
            print()
            print(my_bin(cut))
            print()
            print(my_bin(gene_a))
            print(my_bin(gene_b))
            print()
            print(my_bin(kid1))
            print(my_bin(kid2))

        return Gene(self.min_value, self.max_value, kid1), Gene(self.min_value, self.max_value, kid2)

    def __repr__(self):
        return my_bin(self.gene)

    pass
