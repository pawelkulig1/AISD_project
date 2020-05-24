from graph import Graph

class DecisionGraph(Graph):
    def __init__(self):
        super().__init__()
        pass

    def crossover(self, another: DecisionGraph) -> DecisionGraph:
        pass

    def mutate(self) -> DecisionGraph:
        pass

    def create_embrio(self) -> DecisionGraph:
        pass

    def create_random_graph(self, nodes: int) -> DecisionGraph:
        pass

    
