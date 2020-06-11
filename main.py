from parser import Parser
from decision_graph import DecisionGraph
from procedures import Procedures
from processing_factory import ProcessingFactory
import random

class Simulation:
    def __init__(self, parser: Parser,  \
                       alpha: int,      \
                       beta: float,     \
                       gamma: float,    \
                       delta: float,    \
                       epsilon: float,  \
                       c: float,        \
                       t: float):
        """ 
            parser: Parser - instance of parser
            alpha: int - user provided parameter
            beta:  float - user provided parameter - modificating number of solutions from selection
            gamma: float - user provided parameter - modificating number of solutions from crossing
            delta: float - user provided parameter - modificating number of solutions from mutation
            epsilon: float - user provided parameter - limit of epochs with no progress
            c:      float - user provided parameter - cost weight for fitness function
            t:      float - user provided parameter - time weight for fitness function
            n :    int - number of tasks in graph
            z :    int - number of processing types
            initial_size: int - number of entities in intial population

        """
        self.parser = parser
        self.task_graph = parser.graph
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
        self.c = c
        self.t = t
        self.n = len(self.task_graph.nodes)
        self.z = len(self.parser.procs)
        self.initial_size = self.alpha * self.n * self.z
        self.max_iters = 100 # TODO - for now

    def run(self) -> None:
        self.create_initial_population()
        print(self.population[0])
        for i in range(self.max_iters):
            # print("test123")
            if self.check_stop_condition == True:
                break
            # print("test1234")
            # self.sort_population()
            self.apply_crossover()
            self.apply_mutation()
            self.recalculate_population_fitness()
            print("iteration:", i, self.population[0])

    def recalculate_population_fitness(self):
        self.population = []
        for graph in self.new_population:
            sim = ProcessingFactory(self.parser)
            time, cost = sim.apply(graph)
            self.population.append([graph, 1.0 / (self.t * time + self.c * cost)])
        self.population.sort(key=lambda x: x[1], reverse=True)

    def pick_from_roulette_wheel(self, k=1) -> list:
        return random.choices(self.population, [x[1] for x in self.population], k=k)

    def apply_selection(self) -> None:
        outcome_size = int(round(self.initial_size * self.beta))
        self.new_population.extend(self.pick_from_roulette_wheel(outcome_size))

    def apply_crossover(self) -> None:
        outcome_size = int(round(self.initial_size * self.gamma / 2))
        for i in range(outcome_size):
            parents = self.pick_from_roulette_wheel(k=2)
            child1, child2 = DecisionGraph.crossover(parents[0][0], parents[1][0])
            self.new_population.append(child1)
            self.new_population.append(child2)

    def apply_mutation(self) -> None:
        outcome_size = int(round(self.initial_size * self.delta))
        ready_for_mutation = self.pick_from_roulette_wheel(outcome_size)
        for el in ready_for_mutation:
            self.new_population.append(DecisionGraph.mutate(el[0]))

    def create_initial_population(self) -> None:
        self.population = []
        self.new_population = []
        for i in range(self.initial_size):
            sim = ProcessingFactory(self.parser)
            graph = DecisionGraph.create_random_graph(random.randint(1, self.n))
            time, cost = sim.apply(graph)

            self.population.append([graph, 1.0 / (self.t * time + self.c * cost)])
        self.population.sort(key=lambda x: x[1], reverse=True)

    def check_stop_condition(self) -> bool:
        """ if last epsilon epochs without progress returns true else false"""
        # TODO
        return False 

def main() -> None:
    parser = Parser("grafy/graph_10_2.txt")
    parser.parse()
    
    o_props = [0.5, 0.2, 0.1, 0.1, 0.1]
    c_props = [0.5, 0.25, 0.25]
    Procedures(Parser.instance, o_props, c_props)

    s = Simulation(parser, alpha=20, beta=0.3, gamma=0.3, delta=0.3, epsilon=5, c=1.0, t=1.0)
    s.run()

if __name__ == "__main__":
    main()
