from creature.carnivore import *
from creature.herbivore import *
from res.const import *


def vision_cost(genes):
    r = genes.get(Values.PERCEPTION.id).get_gene_value()
    angle = genes.get(Values.FIELD_OF_VIEW.id).get_gene_value()
    focus = genes.get(Values.FOCUS.id).get_gene_value()
    v = ((r ** 2) * angle) / ((Values.PERCEPTION.high ** 2) * 360)
    return v * focus * 100


def linear_cost(genes, id):
    return genes.get(id).get_gene_proc() * Values.cost


def movement_cost(genes):
    speed = genes.get(Values.SPEED.id).get_gene_value()
    size = genes.get(Values.SIZE.id).get_gene_value()
    force = genes.get(Values.FORCE.id).get_gene_value()
    return (speed ** 2) * (size ** 1.01) + force


def cost_function(entity: Entity):
    genes: Dict[Gene] = entity.genes

    total_cost = vision_cost(genes)

    for stat in {Values.EAT_RANGE}:
        total_cost += linear_cost(genes, stat.id)

    total_cost += movement_cost(genes)
    # print(total_cost)
    return total_cost


class Genetic:
    plants = None
    plants_number = HERBIVORE_EAT_VALUE * 250

    herbivores = None
    herbivores_number = 1000

    carnivores = None
    carnivores_number = 100

    mutation = 5
    cross = 15

    def __init__(self):
        Movement.set_boundary(Movement.edge_distance_pct, 1500, 1500)

        def generate(pop_number, T):
            aux = []
            for _ in range(pop_number):
                aux.append(T())
            return aux

        Genetic.plants = np.asarray(generate(Genetic.plants_number, Plant))
        Genetic.herbivores = np.asarray(generate(Genetic.herbivores_number, Herbivore))
        Genetic.carnivores = np.asarray(generate(Genetic.carnivores_number, Carnivore))

        self.all = np.concatenate([self.carnivores, self.herbivores])

    def load(self):
        car: List[List[Carnivore]] = pickle.load(open("D:\Facultate\TrueLicenta\carnivores.data", "rb"))
        her: List[List[Herbivore]] = pickle.load(open("D:\Facultate\TrueLicenta\herbivores.data", "rb"))
        self.herbivores = []
        self.carnivores = []
        for h in her[-1]:
            entity: Entity = h
            entity.movement.random_pos()
            self.herbivores.append(entity)

        for c in car[-1]:
            entity: Entity = c
            entity.movement.random_pos()
            self.carnivores.append(entity)

        self.herbivores = np.asarray(self.herbivores)
        self.carnivores = np.asarray(self.carnivores)

    def tick(self):
        for creature in self.all:
            creature.update(3, self.all)

        if len(self.plants) < Genetic.plants_number * 0.15:
            plants = [x for x in self.plants if not x.is_ded]
            plants += [Plant() for _ in range(int(self.plants_number * 0.30))]
            self.plants = np.asarray(plants)
        # print(len(plants), len(herbivores), len(carnivores))

    def evolve(self, gen):
        global carnivores, herbivore
        for e in self.all:
            if e.score < MIN_SCORE_VALUE:
                e.is_ded = True

        plants = [x for x in self.plants if not x.is_ded]

        print(f'len(self.herbivores) = {len([None for x in self.herbivores if not x.is_ded])}')
        print(f'len(self.carnivores) = {len([None for x in self.carnivores if not x.is_ded])}')
        print(f'len(self.plants) = {len(plants)}')
        print("plant count", Plant.food_position)
        print("creature count ->", Movement.hashmap)
        print("\n\n")

        carnivores.append(pickle.dumps(self.carnivores))
        herbivore.append(pickle.dumps(self.herbivores))

        new_pop = _evolve_pop(self.carnivores, Carnivore, self.carnivores_number)
        self.carnivores = np.asarray(new_pop)

        new_pop = _evolve_pop(self.herbivores, Herbivore, self.herbivores_number)
        self.herbivores = np.asarray(new_pop)

        self.all = np.concatenate([self.carnivores, self.herbivores])

        print("############", len(self.herbivores), len(self.carnivores))

        for creature in self.all:
            creature.score = 0
            creature.is_ded = False

        self.plants = np.asarray(plants)

        Movement.hashmap = SpatialHash()
        for creature in a.all:
            Movement.hashmap.insert(creature.movement)


best_herbivore = (1, Herbivore(add_to_grid=False))
best_carnivore = (1, Carnivore(add_to_grid=False))


def calculate_fitness(e: Entity):
    s = (e.score + 1 - MIN_SCORE_VALUE * (not e.is_ded) - e.size * e.movement.max_speed)
    c = cost_function(e) + 2 * MIN_SCORE_VALUE * e.is_ded
    return s / c


def _evolve_pop(entities, T: type, pc) -> Union[np.ndarray, list[Entity]]:
    global best_carnivore, best_herbivore, herbivore, carnivores

    pop_count = pc

    creatures = np.asarray(
        [(calculate_fitness(x), x) for x in entities])

    ranking = np.percentile(creatures[:, 0], q=[0, 25, 50, 75, 100])
    print(T)
    print(ranking)

    try:
        if T == Carnivore:
            best_carnivore = (creatures[np.argmax(creatures[:, 0])])

        elif T == Herbivore:
            best_herbivore = (creatures[np.argmax(creatures[:, 0])])
    except:
        pass

    creatures[:, 0] -= np.min(creatures[:, 0])
    creatures[:, 0] += 1
    max_value = np.max(creatures[:, 0])
    p = creatures[:, 0] / (max_value)
    p = p / np.sum(p)

    new_pop: List[Entity] = []

    for creature in np.random.choice(creatures[:, 1], pop_count // 2, p=[x for x in p]):
        new_genes = copy.deepcopy(creature.genes)

        for id, gene in new_genes.items():
            if np.random.randint(100) < Genetic.mutation:
                gene.mutation()

        new_creature = T(generate_gene=False, add_to_grid=False)
        new_creature.update_genes(new_genes)

        new_pop.append(new_creature)

    n = pop_count
    n -= n & 1
    mates = np.random.choice(creatures[:, 1], n)
    mates = mates.reshape(n // 2, 2)

    for male, female in mates:
        genes: Dict[Gene] = male.genes

        kid_1 = copy.deepcopy(genes)
        kid_2 = copy.deepcopy(genes)

        for id, gene in genes.items():
            if np.random.randint(100) < Genetic.cross:
                a, b = gene.cross(female.genes[id])
                kid_1[id] = a
                kid_2[id] = b

        boy = T(generate_gene=False, add_to_grid=False)
        boy.update_genes(kid_1)

        girl = T(generate_gene=False, add_to_grid=False)
        girl.update_genes(kid_2)

        new_pop.extend((boy, girl))

        if len(new_pop) > pop_count:
            break

    new_pop = new_pop[:pop_count]

    return new_pop


save_point = 50
food_gr = 0.99

if __name__ == "__main__":
    a = Genetic()

    import time
    import pickle

    carnivores = []
    herbivore = []

    for generation in range(100000):
        start = time.time()

        for _ in range(Entity.MAX_AGE):
            a.tick()

        a.evolve(generation)

        if generation % save_point == 0:
            with open(r"D:\Facultate\TrueLicenta\data\carnivores.data", "wb") as f:
                pickle.dump(carnivores, f)
            with open(r"D:\Facultate\TrueLicenta\data\herbivores.data", "wb") as f:
                pickle.dump(herbivore, f)

        if (generation // save_point) % 10:
            Genetic.plants_number *= food_gr
        else:
            Genetic.plants_number /= food_gr

        if generation % 10 == 0:
            best_carnivore[1].print_genes()
            best_herbivore[1].print_genes()

        end = time.time()

        print(generation, "TIME ---> ", end - start)

        l = [Plant() for _ in range(len(Genetic.plants), int(Genetic.plants_number))]
        l.extend([p for p in a.plants])
        a.plants = tuple(l)
