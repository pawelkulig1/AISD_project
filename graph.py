class Node:
    def __init__(self, label) -> None:
        """
            Constructor of Node classs which performs Nodes initialization.
            
            Parameters
            ----------
            Only one parameter is label. 
            Label it’s value of the vertex.
        """
        self.label = label
        self.neighbours = {}


class Graph:
    def __init__(self) -> None:
        """
            Constructor of Graph class performs Graph initialization.
            
            Parameters
            ----------
            None
        """
        self.nodes = []

    def find_neighbours(self, label) -> list:
        """
            Function find_neighbours performs finding neighbours of the vertex.
            It’s finding labels of vertex neighbours which was given in parameter. 
            
            Parameters
            ----------
            Label of vertex

            Return
            ----------
            List of labels
        """
        return [[neighbour.label, weight] for neighbour, weight in self.find_node(label).neighbours.items()]

    def DFS(self) -> list:
        """
            Function DFS performs DFS alghoritm.
            
            Parameters
            ----------
            None 
            
            Return
            ----------
            List vertices
        """
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
        """
            Function remove_node performs removing nodes.
            
            Parameters
            ----------
            Label
            
            Return
            ----------
            None
        """
        node = self.find_node(label)
        [prev.neighbours.pop(node) for prev in self.nodes if node in prev.neighbours]
        self.nodes.remove(node)

    def remove_nodes(self, labels: list) -> None:
        """
            Function remove_node performs removing nodes.
            
            Parameters
            ----------
            list of labels
            
            Return
            ----------
            None
        """
        [self.remove_node(label) for label in labels]

    def remove_connection(self, begin, end):
        """
            Function remove_connection performs removing connections.
            
            Parameters
            ----------
            Begin of Edge
            End of Edge
            
            Return
            ----------
            None
        """
        begin_node = self.find_node(begin)
        end_node = self.find_node(end)

        begin_node.neighbours.pop(end_node)

    def remove_connections(self, connections: list) -> None:
        """
            Function remove_connection performs removing connections.
            
            Parameters
            ----------
            List of list of connections (Begin, ends) 
            
            Return
            ----------
            None
        """
        [self.remove_connection(begin, end) for begin, end in connections]

    def is_cyclic(self) -> bool:
        """
            Function is_cyclic performs detection of cycles. 
            
            Parameters
            ----------
            None 
            
            Returns
            ----------
            Bool
        """
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
        """
            Function is_leaf performs detection if vertex is leaf.
            
            Parameters
            ----------
            Label of vertex
            
            Returns
            ----------
            Bool
        """
        return len(self.find_node(label).neighbours) == 0

    def is_leaf_fast(self, node: Node) -> bool:
        """
            Function is_leaf_fast is faster version of is_leaf().
            
            Parameters
            ----------
            Node
            
            Returns
            ----------
            Bool
        """
        return len(node.neighbours) == 0
        
    def add_node(self, label) -> None:
        """
            Function add_node performs adding nodes.
            
            Parameters
            ----------
            Label of vertex 
            
            Return
            ----------
            None
        """
        self.nodes.append(Node(label))

    def add_connection(self, begin: int, end: int, weight: float) -> None:
        """
            Function add_connections performs adding connections.

            Parameters
            ----------
            Begin, end and weight
            
            Return
            ----------
            None
        """
        begin_node = self.find_node(begin)
        end_node = self.find_node(end)

        begin_node.neighbours[end_node] = weight

    def find_node(self, label):
        """
            Function find_node performs finding nodes.
            
            Parameters
            ----------
            Label of vertex
            
            Return
            ----------
            None
        """
        return next(node for node in self.nodes if node.label == label)

    def get_weight(self, begin: int, end: int) -> float:
        """
            Function get_weight performs finding weight of the edge.
            
            Parameters
            ----------
            Begin of the Edge: int
            End of the Edge: int
            
            Return
            ----------
            Float
        """
        begin_node = self.find_node(begin)
        end_node = self.find_node(end)
        return begin_node.neighbours[end_node]

    def get_weight_fast(self, begin: Node, end: Node):
        """
            Function get_weight_fast is faster version of get_weight().
            
            Parameters
            ----------
            Begin of the Edge: Node
            End of the Edge: Node
            
            Return
            ----------
            Float
        """
        return begin.neighbours[end]

    def find_parents(self, node: int) -> list:
        """
            Function find_parents performs finding parents of the node.
            
            Parameters
            ----------
            Node 
            
            Return
            ----------
            List of nodes
        """
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
        """
            Function get_all_children performs finding children of the node. 
            
            Parameters
            ----------
            Node
            
            Return
            ----------
            List of nodes
        """
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

