from graph import Graph, Node
from channel import Channel
import copy
import time

class Path:
    def __init__(self, begin: Node, end: Node, weight: float):
        self.begin = begin
        self.end = end
        self.weight = weight#graph.get_weight_fast(begin, end)
        
    def getWeight(self):
        return self.weight

    def __str__(self):
        return "Path: " + str(self.begin.label) + "->" + str(self.end.label)

    def __eq__(self, item):
        if self.begin == item.begin and self.end == item.end:
            return True
        return False


class TaskGraph(Graph):
    # CRITICAL_COUNTER = 0
    def __init__(self):
        super().__init__()
        self.paths = []

    def find_critical_path(self) -> list:
        # TaskGraph.CRITICAL_COUNTER += 1
        # start = time.time()
        all_paths = self.find_all_paths()
        all_converted = []
        for path in all_paths:
            if len(path) < 2:
                continue
            arr = [Path(path[i], path[i+1], self.get_weight_fast(path[i], path[i+1])) for i in range(len(path) - 1)]
            all_converted.append([arr, self.calculate_cost(arr)])
        
        #print(all_converted)
        critical_path = []
        while len(critical_path) < len(self.nodes) - 1:
            all_converted.sort(key=lambda x: x[1], reverse=True)
            #print(self.calculate_cost(all_converted[0][0]))
            critical_route = all_converted[0][0][0]
            critical_path.append(critical_route)
            for p in all_converted:
                if critical_route in p[0]:
                    p[0].remove(critical_route)
                    p[1] -= critical_route.getWeight()
                    
        # Root always first
        ret = [self.nodes[0].label]
        ret.extend([x.end.label for x in critical_path])

        # print("find critical path time: ", TaskGraph.CRITICAL_COUNTER, time.time() - start)
        return ret
    
    def calculate_cost(self, path: list) -> float:
        # if len(path) == 0:
        #     return -1
        return sum([p.getWeight() for p in path])

    def find_all_paths(self) -> list:
        starting_node = self.nodes[0]
        self._find_all_paths(starting_node, [starting_node], [starting_node])
        for i, path in enumerate(self.paths):
            if not self.is_leaf_fast(path[-1]):
                self.paths.remove(path)
        return self.paths

    def _find_all_paths(self, node, visited=[], path=[]) -> list:
        found_neighs = node.neighbours.keys()
        for neigh in found_neighs:
            if neigh not in visited:
                # Make copy of path to allow traversing with and without stored path
                path_copy = copy.copy(path)
                path_copy.append(neigh)

                self.paths.append(path_copy)

                # Make copy of visited to allow traversing with and without stored visited
                vis_copy = copy.copy(visited)
                
                # Recursively call invoke find_all_paths
                self._find_all_paths(neigh, vis_copy, path_copy)


if __name__ == "__main__":
    tg = TaskGraph()
    tg.add_node(0)
    tg.add_node(1)
    tg.add_node(2)
    tg.add_node(3)
    tg.add_node(4)
    tg.add_node(5)
    tg.add_node(6)
    tg.add_connection(0, 1, 1)
    tg.add_connection(1, 2, 2)
    tg.add_connection(0, 3, 3)
    tg.add_connection(1, 4, 4)
    tg.add_connection(1, 5, 5)
    tg.add_connection(5, 6, 6)

    found_paths = tg.find_all_paths()
    
    critical = tg.find_critical_path()
    [print(n, end=", ") for n in critical]