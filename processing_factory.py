from collections import defaultdict
import random
from parser import Parser
from graph import Node
from processor import Processor
from decision_graph import DecisionGraph, DecisionNode
#from task_graph import TaskGraph, TaskNode
#delete later
from channel import Channel


MAX = 1e10
class ProcessingFactory:
    class ScheduledTask:
        def __init__(self, parser: Parser, processor: Processor, task: Node) -> None:
            self.parser = parser
            self.task = task
            self.processor = processor
            self.default_time = -1
            self.cost = -1
            self.calculate()
            self.time = self.default_time
            self.enabled = False
            self.delayed = False
    
        def calculate(self) -> None:
            self.default_time = self.parser.times[self.task][self.processor.index]
            self.cost = self.parser.costs[self.task][self.processor.index]
    
        def getTime(self) -> int:
            return self.time
    
        def getDefaultTime(self) -> int:
            return self.default_time
    
        def getCost(self) -> int:
            return self.cost

        def passTime(self, time: int) -> int:
            if self.delayed:
                self.delayed = None
                return

            if self.enabled:
                self.time -= time

        def enable(self, delay=False):
            self.enabled = True
            if self.delayed == False:
                self.delayed = delay

    def __init__(self, parser: Parser) -> None: #, #task_graph, processors, comms = []) -> None:
        self.task_graph = parser.graph
        self.processors = parser.procs
        self.comms = parser.comms
        self.parser = parser
        self.application = defaultdict(list)
        self.done_tasks = []
        self.location = []
        self.done_task = []

    def apply_random(self) -> None:
        for task in self.task_graph.DFS():
            self.application[random.choice(self.processors)].append(task)
        #now on each node tasks should be sorted finding critical path TODO

    def apply(self, decision_graph: DecisionGraph) -> None:
        #takes decision graph and applies them to processors

        all_tasks = self.task_graph.nodes
        last_node = None
        for n in decision_graph.DFS():
            #pick tasks for nodes keeping in mind propabilities and graph structure
            node = decision_graph.find_node(n)
            parent = decision_graph.find_parents(node)
            print(node, parent)
            if parent:
                parent = parent[0]
                picked_tasks = random.sample(parent.tasks, k=round(node.propability * len(parent.tasks)))
                assert len(picked_tasks) <= len(parent.tasks)
            else:
                picked_tasks = random.sample(all_tasks, k=round(node.propability * len(all_tasks)))
             
            node.tasks = picked_tasks
            [print(p) for p in picked_tasks]
            

    def find_operation_1(self, task):
        return self.parser.costs.index(min(self.parser.costs[task][:]))

    def find_operation_2(self, task):
        return self.parser.times[task][:].index(min(self.parser.times[task][:]))

    def find_operation_3(self, task):
        min_val = MAX
        min_ind = -1
        for i, p in enumerate(self.processors):
            val = self.parser.times[task][i] * self.parser.costs[task][i]
            if val < min_val:
                min_val = val
                min_ind = i

        assert min_ind != -1
        return min_ind

    def find_operation_4(self, task):
        #TODO
        pass

    def find_operation_5(self, task):
        min_l = MAX
        min_ind = -1
        for i, key in enumerate(self.application.keys()):
            temp = len(self.pallication[key])
            if temp < min_l:
                min_l = temp
                min_ind = i

        assert min_ind != -1
        return min_ind

    #def find_comm_1(self, task):
    #def find_comm_2(self, task):
    #def find_comm_3(self, task):

    

    def simulate(self) -> (int, int):
        sums = [0 for i in range(10)]
        iteration = 0
        time = 0
        cost = 0
        queue = [None for _ in self.processors]
        done = False
        while len(self.done_tasks) < len(self.task_graph.nodes):
            iteration +=1

            #done = True
            for qi, proc in enumerate(self.processors):
                if len(self.application[proc]) > 0 and queue[qi] == None:
                    task = self.application[proc].pop(0)
                    queue[qi] = ProcessingFactory.ScheduledTask(self.parser, proc, task)
                 #   print("queue: ", qi, " -> ", task)
                    cost += queue[qi].getCost()
             #       done = False
            
            min_construction_time = min(queue, key=lambda x: x.getTime() if x else MAX).getTime()
            min_time = min_construction_time
            transfer_target = -1

            for queue_index, queue_el in enumerate(queue):
                if not queue_el:
                    continue
                parents = self.task_graph.find_parents(queue_el.task)
                #print(queue_el.task, parents)
                if not parents:
                    #queue_el.passTime(min_time)
                    queue_el.enabled = True

                #all parents have to be done.
                #if parents:
                #    print("intersections:", set(parents), set(self.done_tasks), set(parents).intersection(set(self.done_tasks)))
                if parents and set(parents).intersection(set(self.done_tasks)) == set(parents) and len(self.done_tasks) > 0:
               #     print("transfer needed")
                     
                    transfer_time = 0
                    #resources from all parents have to be on this node
                    all_here = True
                    for parent in parents:
                        ind = self.done_tasks.index(parent)
                        if self.location[ind] != queue_index and ind in self.done_tasks:
                            all_here = False
                            transfer_time += self.task_graph.get_weight(parent, queue_el.task) / 1 #TODO
              #              print("transfering:", self.location[ind], ind, " -> ", queue_index, ind)
                            self.location[ind] = queue_index
                            #transfer_target = queue_index
                        
                    queue_el.enable(True)
                        
                    if all_here:
             #           print("all resources in place!")
                        queue_el.enable()
                    if queue_el and transfer_time > 0:
                        min_time = transfer_time
                    elif queue_el:
                        min_time = min_construction_time
                        
            for queue_el in queue:
                if queue_el:
                    queue_el.passTime(min_time)

            #if transfer_target != -1:
            #    queue[transfer_target].enabled = True
            time += min_time
            #print("TIME:", time, min_time, iteration, self.done_tasks)
            sums[iteration%len(sums)] = sum([x.getTime() for x in queue if x])#, key=lambda x: x.getTime() if x else 0) 
             
            for i, e in enumerate(queue):
                if queue[i] != None and queue[i].getTime() <= 0:
                    #done has task which were finished, location has nodes on which resources are currently stored
                    self.done_tasks.append(queue[i].task)
                    self.location.append(i)
                    queue[i] = None

            #print("queue after constructing:", queue) 
            #print(sums)
            if sum(sums)/len(sums) == sums[-1]:
                return MAX, MAX
            #assert iteration < 1000 #safety
        return time, cost


if __name__ == "__main__":
    parser = Parser("grafy/graph_10_2.txt")
    parser.parse()

    #random application and simulation
    pf = ProcessingFactory(parser)
    pf.apply_random()
    #print(pf.application)
    print(pf.simulate())

    #random application from decision tree:

    #dg = DecisionGraph()
    #dg.add_node(DecisionNode(0, Channel.instances[0], 1.0))
    #dg.add_node(DecisionNode(1, Channel.instances[0], 0.3))
    #dg.add_node(DecisionNode(2, Channel.instances[0], 0.2))
    #dg.add_connection(0, 1, 0)
    #dg.add_connection(1, 2, 0)

    #pf = ProcessingFactory(parser)
    #pf.apply(dg)

    #dg = DecisionGraph()
    #dg.add_node(DecisionNode(0, Channel.instances[0], 1.0))
    #dg.add_node(DecisionNode(1, Channel.instances[0], 0.3))
    #dg.add_node(DecisionNode(2, Channel.instances[0], 0.2))
    #dg.add_node(DecisionNode(3, Channel.instances[0], 0.5))
    #dg.add_connection(0, 1, 0)
    #dg.add_connection(1, 2, 0)
    #dg.add_connection(0, 3, 0)

    #pf = ProcessingFactory(parser)
    #pf.apply(dg)
        
