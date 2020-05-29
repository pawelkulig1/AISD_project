from graph import Graph
import random

class DecisionGraph(Graph):

    def __init__(self) -> None:
        self.nodes = []

    def crossover(self, parent_1, parent_2):
        chromosome_length = len(parent_1)
        crossover_point = random.randint(1, chromosome_length - 1)
        child_1 = (parent_1[0:crossover_point], parent_2[crossover_point:])
        child_2 = (parent_2[0:crossover_point], parent_1[crossover_point:])
        return child_1, child_2

    def mutate(self, population, mutation_probability):
        random_mutation_array = random.random(size=(population.shape))

        random_mutation_boolean = \
            random_mutation_array <= mutation_probability

        population[random_mutation_boolean] = \
            (population[random_mutation_boolean])

        return population

    def create_embrio(self):
        embrio = random.choice()
        return embrio

    def create_random_graph(self, n, p, lower_weight, upper_weight):

        g = graphs.RandomGNP(n, p)
        m = g.num_edges()
        weights = [random.randint(lower_weight, upper_weight) for r in range(m)]
        uw_edges = g.edges()
        w_edges = [(uw_edges[i][0], uw_edges[i][1], weights[i]) for i in range(m)]

        return Graph(w_edges, weighted=True)