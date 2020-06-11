class Node:
    def __init__(self, label) -> None:
        self.label = label
        self.neighbours = {}


class Graph:
    def __init__(self) -> None:
        self.nodes = []

    def find_neighbours(self, label) -> list:
        return [[neighbour.label, weight] for neighbour, weight in self.find_node(label).neighbours.items()]

    def DFS(self) -> list:
        visited = []
        result = []

        for node in self.nodes:
            if node not in visited:
                self.__DFS(node, visited, result)

        return result

    def __DFS(self, node, visited, result):
        visited.append(node)
        result.append(node.label)

        for neighbour in node.neighbours:
            if neighbour not in visited:
                self.__DFS(neighbour, visited, result)

    def remove_node(self, label):
        node = self.find_node(label)
        [prev.neighbours.pop(node) for prev in self.nodes if node in prev.neighbours]
        self.nodes.remove(node)

    def remove_nodes(self, labels: list) -> None:
        [self.remove_node(label) for label in labels]

    def remove_connection(self, begin, end):
        begin_node = self.find_node(begin)
        end_node = self.find_node(end)

        begin_node.neighbours.pop(end_node)

    def remove_connections(self, connections: list) -> None:
        [self.remove_connection(begin, end) for begin, end in connections]

    def is_cyclic(self) -> bool:
        visited = []

        for node in self.nodes:
            if node not in visited:
                if self.__is_cyclic(node, visited):
                    return True

        return False

    def __is_cyclic(self, node, visited):
        visited.append(node)

        for neighbour in node.neighbours:
            if neighbour in visited:
                return True
            elif self.__is_cyclic(neighbour, visited):
                return True

        visited.remove(node)
        return False

    def is_leaf(self, label) -> bool:
        return len(self.find_node(label).neighbours) == 0

    def is_leaf_fast(self, node: Node) -> bool:
        return len(node.neighbours) == 0
        
    def add_node(self, label) -> None:
        self.nodes.append(Node(label))

    def add_connection(self, begin: int, end: int, weight: float) -> None:
        begin_node = self.find_node(begin)
        end_node = self.find_node(end)

        begin_node.neighbours[end_node] = weight

    def find_node(self, label):
        return next(node for node in self.nodes if node.label == label)

    def get_weight(self, begin: int, end: int) -> float:
        begin_node = self.find_node(begin)
        end_node = self.find_node(end)
        return begin_node.neighbours[end_node]

    def get_weight_fast(self, begin: Node, end: Node):
        return begin.neighbours[end]

    def find_parents(self, node: int) -> list:
        parents = []
        assert isinstance(node, int)
        _node = self.find_node(node)
        for graph_node in self.nodes:
            #print(_node, graph_node.neighbours.keys())
            if _node in graph_node.neighbours.keys():
                parents.append(graph_node.label)

        if len(parents) > 0:
            return parents
        return None

    def get_all_children(self, node: int) -> list:
        children = []
        self._get_all_children(self.find_node(node), children)
        return children
    
    def _get_all_children(self, node: Node, children = []) -> list:
        for neigh in node.neighbours.keys():
            if neigh.label not in children:
                children.append(neigh.label)
                self._get_all_children(neigh, children)
            else:
                return

    def __str__(self):
        out = ""
        for node in self.nodes:
            out += str(node.label) + ": "
            for neigh in node.neighbours.keys():
                out += str(neigh.label) + ", "
            out += "\n"
        return out

if __name__ == "__main__":
    dg = Graph()
    
    dg.add_node(0)
    dg.add_node(1)
    dg.add_node(2)
    dg.add_node(3)
    dg.add_connection(0, 1, 0)
    dg.add_connection(1, 2, 0)
    dg.add_connection(0, 3, 0)



    [print(x.label) for x in dg.get_all_children(0)]

