class Node:
    def __init__(self) -> None:
        pass
    
class Connection:
    def __init__(self) -> None:
        pass

class Graph:
    def __init__(self) -> None:
        self.nodes = []
        self.connections = []

    def find_neighbours(self) -> list:
        pass

    def DFS(self) -> list:
        pass

    def remove_nodes(self, nodes: list) -> None:
        pass

    def remove_connections(self, connections: list) -> None:
        pass

    def is_cyclic(self) -> bool:
        pass

    def is_leaf(self, node) -> bool:
        pass

    def add_node(self, node: Node) -> None:
        pass

    def add_connection(self, connection: Connection) -> None:
        pass