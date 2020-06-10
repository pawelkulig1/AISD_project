from graph import Graph, Node
from channel import Channel
from parser import Parser
from procedures import Procedures
import random
import logging

class DecisionNode(Node):
    def __init__(self, label: int, propability: float, t_strategy=None, c_strategy=None):
        super().__init__(label)

        # self.channel = channel
        self.check_propability(propability)
        self.propability = propability
        self.tasks = []
        self.connections = []
        self.task_strategy = t_strategy
        self.comm_strategy = c_strategy

    def check_propability(self, propability):
        assert propability >= 0.01
        assert propability <= 1.0

    def __str__(self):
        return "DecisionNode:\n label " + str(self.label) + "\n propability: " + str(self.propability)

class DecisionGraph(Graph):
    def __init__(self) -> None:
        super().__init__()

    @staticmethod
    def crossover(self, parent_1: Graph, parent_2: Graph) -> (Graph, Graph):
        #TODO
        pass

    @staticmethod
    def mutate(self, graph) -> Graph:
        random_node = random.sample(graph.nodes, k=1)
        random_node.task_strategy = Procedures.instance.get_oper()
        random_node.comm_strategy = Procedures.instance.get_comm()
        return graph

    @staticmethod
    def create_random_graph(count):
        connected = []
        # temp_nodes = []
        dg = DecisionGraph()
        pr = Procedures.instance

        dg.add_node(DecisionNode(0, 1, pr.get_oper(), pr.get_comm()))
        for i in range(1, count):
            dg.add_node(DecisionNode(i, (random.random() * 0.9 + 0.1), pr.get_oper(), pr.get_comm()))

        dg.add_connection(0, 1, 0)
        connected.extend([0, 1])
        for n in dg.nodes:
            if n.label in connected:
                continue
            else:
                dest = random.sample(connected, k=1)[0]
                logging.debug(n.label, " -> ", dest)
                dg.add_connection(n.label, dest, 0)
                connected.append(n.label)
        
        return dg

    def add_node(self, node: DecisionNode):
        self.nodes.append(node)


if __name__ == "__main__":
    o_props = [0.5, 0.2, 0.1, 0.1, 0.1]
    c_props = [0.5, 0.25, 0.25]
    Procedures(Parser.instance, o_props, c_props)
    graph = DecisionGraph.create_random_graph(15)
    print(len(graph.nodes))
    