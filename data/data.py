import pickle

import numpy as np
from matplotlib import pyplot as plt

from algoritmi.Genetic import cost_function
from creature.carnivore import *
from creature.herbivore import *

from algoritmi.Genetic import calculate_fitness

c: List[List[Carnivore]] = pickle.load(open("D:\Facultate\TrueLicenta\din\carnivores.data", "rb"))

h: List[List[Herbivore]] = pickle.load(open("D:\Facultate\TrueLicenta\data\herbivores.data", "rb"))

x = c[0][0]

f_score = lambda x: x.score

field_of_view = 0
perception = 1

max_speed = 2
size = 3

alignment_importance = 4
separation_importance = 5
cohesion_importance = 6
avoid_importance = 7


def get_gene_data(e: Entity):
    return (e.movement.field_of_view,
            e.movement.perception,

            e.movement.max_speed,
            e.size,

            e.alignment_importance,
            e.separation_importance,
            e.cohesion_importance,
            e.avoid_importance)


info_score_c = []
info_score_h = []

fitness_c = []
fitness_h = []

info_gene_c = []
info_gene_h = []

info_cost_c = []
info_cost_h = []

info_fitness_c = []
info_fitness_h = []




for i in range(len(c)):
    # carnivores = c[i]
    # herbivores = h[i]

    carnivores = pickle.loads(c[i])
    herbivores = pickle.loads(h[i])

    score_c = np.array(list(map(f_score, carnivores)))
    score_h = np.array(list(map(f_score, herbivores)))

    info_score_c.append(score_c)
    info_score_h.append(score_h)

    cost_c = np.array(list(map(cost_function, carnivores)))
    cost_h = np.array(list(map(cost_function, herbivores)))

    info_cost_c.append(cost_c)
    info_cost_h.append(cost_h)

    alive_c = len(list(filter(lambda x: x.is_ded, carnivores)))
    alive_h = len(list(filter(lambda x: x.is_ded, herbivores)))

    carnivores = sorted(carnivores, key=f_score)
    herbivores = sorted(herbivores, key=f_score)

    fitness_c = list(map(calculate_fitness,carnivores))
    fitness_h = list(map(calculate_fitness, herbivores))

    info_fitness_c.append(fitness_c)
    info_fitness_h.append(fitness_h)

    gene_data_c = list(map(get_gene_data, carnivores))
    gene_data_h = list(map(get_gene_data, herbivores))

    info_gene_c.append(gene_data_c)
    info_gene_h.append(gene_data_h)

line = [x for x in range(5, len(info_score_c))]

info_score_c = np.asarray(info_score_c)
fitness_c = np.asarray(fitness_c)

info_gene_c = np.asarray(info_gene_c)
info_gene_h = np.asarray(info_gene_h)

info_fitness_c = np.asarray(info_fitness_c)
info_fitness_h = np.asarray(info_fitness_h)

def deseneaza(data):
    data = data[10:]
    print(data)
    line = [x for x in range(len(data),10)]

    de_desenat = []
    for l in data:
        p = np.percentile(l, q=[30, 50, 70, 90])
        de_desenat.append(p)

    de_desenat = np.asarray(de_desenat)

    plt.figure()
    plt.plot(line, de_desenat[: 0], 'salmon')
    plt.plot(line, de_desenat[:, 1], 'gold', linestyle='dotted')
    plt.plot(line, de_desenat[:, 2], 'yellowgreen', linestyle='dotted')
    plt.plot(line, de_desenat[:, 3], 'forestgreen')
    plt.grid()
    plt.show()


def deseneaza_best_worst_avg(data, t="t"):
    line = [x  for x in range(len(data))]

    de_desenat = []
    for l in line:
        l = data[l]
        p = np.percentile(l, q=[30, 50, 80])
        top_5 = np.average(l[int(len(l) * 0.95):])
        de_desenat.append([p[0], p[1], p[2], top_5])

    de_desenat = np.asarray(de_desenat)

    plt.figure()

    fig, (ax1,ax2) = plt.subplots(2)

    fig.suptitle(t)

    ax1.set_ylabel("Valoare")
    ax1.plot(line, de_desenat[:, 0], 'salmon', linestyle='dotted',label=' 30%')
    ax1.plot(line, de_desenat[:, 1], 'gold' ,label="Media")
    ax1.plot(line, de_desenat[:, 2], 'forestgreen', linestyle='dotted',label = "80%")

    ax1.fill_between(line, de_desenat[:, 0] ,de_desenat[:, 2], color="yellow", alpha=0.1)
    ax1.legend()
    ax1.grid()

    ax2.set_xlabel("Generatie")
    ax2.set_ylabel("Valoare")
    ax2.plot(line, de_desenat[:, 3], 'blue',label="Top 5% scor")
    ax2.legend()
    ax2.grid()


    plt.savefig(t + ".png")
    plt.show()


#carnivore
deseneaza_best_worst_avg(info_gene_c[:, :, perception], "Evolutia perceptiei la  carnivore")
deseneaza_best_worst_avg(info_gene_c[:, :, field_of_view], "Evolutia unghiului de viziune la carnivore")

deseneaza_best_worst_avg(info_gene_c[:, :, max_speed], "Evolutia vitezei la carnivore")
deseneaza_best_worst_avg(info_gene_c[:, :, size], "Evolutia marimii la carnivore")

deseneaza_best_worst_avg(info_gene_c[:, :, alignment_importance], "Importanta functiei de aliniere la carnivore")
deseneaza_best_worst_avg(info_gene_c[:, :, separation_importance], "Importanta functiei de separare la carnivore")
deseneaza_best_worst_avg(info_gene_c[:, :, cohesion_importance], "Importanta functiei de coeziune la carnivore")

deseneaza_best_worst_avg(info_fitness_c[:], "Fitness carnivore")


#
# #erbivore

deseneaza_best_worst_avg(info_gene_h[:, :, perception], "Evolutia perceptiei la  erbvivore")
deseneaza_best_worst_avg(info_gene_h[:, :, field_of_view], "Evolutia unghiului de viziune la  erbvivore")

deseneaza_best_worst_avg(info_gene_h[:, :, max_speed], "Evolutia vitezei la erbvivore")
deseneaza_best_worst_avg(info_gene_h[:, :, size], "Evolutia marimii la erbvivore")

deseneaza_best_worst_avg(info_gene_h[:, :, alignment_importance], "Importanta functiei de aliniere la erbvivore")
deseneaza_best_worst_avg(info_gene_h[:, :, separation_importance], "Importanta functiei de separare la erbvivore")
deseneaza_best_worst_avg(info_gene_h[:, :, cohesion_importance], "Importanta functiei de coeziune erbvivore")

deseneaza_best_worst_avg(info_fitness_h[:], "Fitness erbivore")
