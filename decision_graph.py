from graph import Graph, Node
from channel import Channel
from parser import Parser
from procedures import Procedures
import random
import logging
import copy

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
    def crossover(parent_1: Graph, parent_2: Graph) -> (Graph, Graph):
        offset = 1000 #to avoid label conflict 

        if len(parent_1.nodes) == 1 or len(parent_2.nodes) == 1:
            return parent_1, parent_2

        child_1 = copy.deepcopy(parent_1)
        child_2 = copy.deepcopy(parent_2)
        point1n = random.sample(child_1.nodes[1:], k=1)[0]
        point2n = random.sample(child_2.nodes[1:], k=1)[0]

        point1 = point1n.label
        point2 = point2n.label

        logging.debug("points: ", point1, point2)

        g1_parents = child_1.find_parents(point1)
        g2_parents = child_2.find_parents(point2)

        g1_children_labels = child_1.get_all_children(point1)
        g2_children_labels = child_2.get_all_children(point2)

        g1_children = copy.copy([child_1.find_node(n) for n in g1_children_labels])
        g2_children = copy.copy([child_2.find_node(n) for n in g2_children_labels])

        #remove nodes from source graphs
        child_1.remove_node(point1)
        child_2.remove_node(point2)

        child_1.remove_nodes(g1_children_labels)
        child_2.remove_nodes(g2_children_labels)

        #add nodes to destination graphs
        child_1.add_real_node(DecisionNode( point2 + offset, \
                                            point2n.propability, \
                                            point2n.task_strategy, \
                                            point2n.comm_strategy))

        child_2.add_real_node(DecisionNode(  point1 + offset, \
                                        point1n.propability, \
                                        point1n.task_strategy, \
                                        point1n.comm_strategy))

        for n in g2_children:
            child_1.add_real_node(DecisionNode(n.label + offset, n.propability, n.task_strategy, n.comm_strategy))
        
        for n in g1_children:
            child_2.add_real_node(DecisionNode(n.label + offset, n.propability, n.task_strategy, n.comm_strategy))

        #add connections from parents to added nodes
        if g1_parents:
            for p in g1_parents:
                child_1.add_connection(p, point2 + offset, 0)

        if g2_parents:
            for p in g2_parents:
                child_2.add_connection(p, point1 + offset, 0)

        #add connections from added node to it's children
        for child in point1n.neighbours.keys():
            child_2.add_connection(point1 + offset, child.label + offset, 0)

        for child in point2n.neighbours.keys():
            child_1.add_connection(point2 + offset, child.label + offset, 0)

        #add all connections between added children
        for child in g1_children:
            for neigh in child.neighbours.keys():
                child_2.add_connection(child.label + offset, neigh.label + offset, 0)

        for child in g2_children:
            for neigh in child.neighbours.keys():
                child_1.add_connection(child.label + offset, neigh.label + offset, 0)

        #recalculate labels
        for i, n in enumerate(child_1.nodes):
            n.label = i

        for i, n in enumerate(child_2.nodes):
            n.label = i

        return child_1, child_2

    @staticmethod
    def mutate(graph) -> Graph:
        random_node = random.sample(graph.nodes, k=1)[0]
        random_node.task_strategy = Procedures.instance.get_oper()
        random_node.comm_strategy = Procedures.instance.get_comm()
        return graph

    @staticmethod
    def create_random_graph(count):
        connected = []
        # temp_nodes = []
        dg = DecisionGraph()
        pr = Procedures.instance

        dg.add_real_node(DecisionNode(0, 1, pr.get_oper(), pr.get_comm()))
        for i in range(1, count):
            dg.add_real_node(DecisionNode(i, (random.random() * 0.9 + 0.1), pr.get_oper(), pr.get_comm()))

        if count > 1:
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

    def add_real_node(self, node: DecisionNode):
        self.nodes.append(node)


if __name__ == "__main__":
    o_props = [0.5, 0.2, 0.1, 0.1, 0.1]
    c_props = [0.5, 0.25, 0.25]
    Procedures(Parser.instance, o_props, c_props)
    
    dg1 = DecisionGraph()
    dg1.add_node(0)
    dg1.add_node(1)
    dg1.add_node(2)
    dg1.add_node(3)
    dg1.add_node(4)
    dg1.add_node(5)
    dg1.add_node(6)
    dg1.add_connection(0, 1, 0)
    dg1.add_connection(1, 2, 0)
    dg1.add_connection(0, 3, 0)
    dg1.add_connection(1, 4, 0)
    dg1.add_connection(1, 5, 0)
    dg1.add_connection(5, 6, 0)

    dg2 = copy.deepcopy(dg1)
    g1 = DecisionGraph.mutate(dg1)
    print(g1)
    g1, g2 = DecisionGraph.crossover(dg1, dg2)

    print(g1)
    print
    print(g2)
    # print(len(graph.nodes))
    