from collections import defaultdict, Counter
import random
from parser import Parser
from graph import Node
from processor import Processor
from decision_graph import DecisionGraph, DecisionNode
from channel import Channel
from procedures import Procedures
import copy
import logging


MAX = 1e10
class ProcessingFactory:
    class ScheduledTask:
        def __init__(self, parser: Parser, processor: Processor, task: Node) -> None:
            """
            SheduledTask is helper class to keep information 
            about task in queue.

            Parameters
            ----------
            parser: Parser
                Input graph data parser
            processor: Processor
                Processor which will execute task
            task: Node
                Node from graph that this class will be representing

            Returns
            ----------
            None
            """
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
            """
            Initializes values: time and cost from parser.

            Parameters
            ----------
            None

            Returns
            ----------
            None
            """
            self.default_time = self.parser.times[self.task][self.processor.index]
            self.cost = self.parser.costs[self.task][self.processor.index]
    
        def getTime(self) -> int:
            return self.time
    
        def getDefaultTime(self) -> int:
            return self.default_time
    
        def getCost(self) -> int:
            return self.cost

        def passTime(self, time: int) -> None:
            """
            Function to pass time in object (to construct it). 
            If delayed set to true do not pass time 
            but change internal state to pass in next run.
            If task is disabled (cannot be built) time won't pass.

            Parameters
            ----------
            time: int
                Amount of time to pass

            Returns
            ----------
            None
            """
            if self.delayed == True:
                self.delayed = None
                return

            if self.enabled == True:
                self.time -= time

        def enable(self, delay=False) -> None:
            """
            Function to enable task in queue to 
            allow it's construction (time passing).
            Parameters
            ----------
            delay: bool
                Flag if delay will be performed

            Returns
            ----------
            None
            """
            self.enabled = True
            if self.delayed == False:
                self.delayed = delay

    def __init__(self, parser: Parser) -> None:
        self.task_graph = parser.graph
        self.processors = parser.procs
        self.comms = parser.comms
        self.parser = parser
        self.reset()

    def reset(self):
        self.application = defaultdict(list)
        self.transfer = [[None for _, _ in enumerate(self.processors)] for _, _ in enumerate(self.processors)]
        self.done_tasks = []
        self.location = []
        self.done_task = []

    def apply_random(self, critical=True) -> None:
        """
            Creates initial task application to 
            nodes (embrio), it is done randomly
            but with DFS search to minimize chance 
            of getting impossible graphs

            Parameters
            ----------
            None

            Returns
            ----------
            None
        """
        task_order = None
        if critical == True:
            task_order = self.task_graph.find_critical_path()
        else:
            task_order = self.task_graph.DFS()
        for task in task_order:
            self.application[random.choice(self.processors).index].append(task)
        
        for proc1, _ in enumerate(self.processors):
            for proc2, _ in enumerate(self.processors):
                if proc1 == proc2:
                    continue
                self.transfer[proc1][proc2] = copy.copy(random.choice(self.parser.comms))
        logging.debug(self.transfer)

    def move_task(self, task, where):
        """
            Moves task from one processor to another

            Parameters
            ----------
            task: int
                Task label to move
            where: int
                index of processor where to move task

            Returns
            ----------
            None
        """
        for key in self.application.keys():
            if task in self.application[key]:
                self.application[key].remove(task)

        self.application[where].append(task)


    def sort_tasks_with_critical_order(self):
        critical_path = self.task_graph.find_critical_path()
        new_application = defaultdict(list)
        for task in critical_path:
            for key in self.application.keys():
                if task in self.application[key]:
                    new_application[key].append(task)
        
        self.application = new_application

    def alter_connection(self, conn, new_conn):
        """
            Changes connection between processors

            Parameters
            ----------
            conn: int
                Task to move
            new_conn: int
                new connection index in comms in parser

            Returns
            ----------
            None
        """
        conn = copy.copy(self.parser.comms[new_conn])
        return conn

    def apply(self, decision_graph: DecisionGraph) -> None:
        """
            Applies graph to random task application, 
            performs all required tasks alterings 
            according to graph structure and 
            strategies in nodes

            Parameters
            ----------
            decision_graph: DecisionGraph
                Graph with altering structure

            Returns
            ----------
            None
        """
        #takes decision graph and applies them to processors
        self.apply_random(False)
        logging.debug("application1:", self.application)
        logging.debug("connections1:", self.transfer)

        Procedures.instance.set_application(self.application)

        all_tasks = self.task_graph.nodes
        all_connections = [i for sub in self.transfer for i in sub if i]
        for n in decision_graph.DFS():
            #pick tasks for nodes keeping in mind propabilities and graph structure
            node = decision_graph.find_node(n)
            parent = decision_graph.find_parents(n)
            logging.debug(node, parent)

            if parent:
                #If node has parent use it's tasks to pick from
                parent = decision_graph.find_node(parent[0])
                picked_tasks = random.sample(parent.tasks, k=round(node.propability * len(parent.tasks)))
                assert len(picked_tasks) <= len(parent.tasks)
                picked_connections = random.sample(parent.connections, k=round(node.propability * len(parent.connections)))
                assert len(picked_connections) <= len(parent.connections)
            else:
                #If node has no parents pick random elements from all tasks according to propability value
                picked_tasks = random.sample(all_tasks, k=round(node.propability * len(all_tasks)))
                picked_connections = random.sample(all_connections, k=round(node.propability * len(all_connections)))

            node.tasks = picked_tasks
            node.connections = picked_connections

            #pick tasks according to operation (strategy) in this node
            for task in picked_tasks:
                self.move_task(task.label, node.task_strategy(task.label))

            #pick connection according to comm (strategy) in this node
            for conn in picked_connections:
                picked = node.comm_strategy(self.transfer)
                conn = self.alter_connection(conn, picked)

        logging.debug("application2:", self.application)
        logging.debug("connections2:", self.transfer)

        self.sort_tasks_with_critical_order()
        return self.simulate()

    def simulate(self) -> (int, int):
        """
            Main function performing simulation, 
            responsible for calculating time and cost 
            for specific graph, including parallel 
            execution and transmission times 
            with transmission requirements. 

            Parameters
            ----------
            None

            Returns
            ----------
            (int, int)
                Tuple consisting of time and cost

        """
        sums = [0 for i in range(10)]
        iteration = 0
        time = 0
        cost = 0

        # initialize queues list
        queue = [None for _ in self.processors]
        while len(self.done_tasks) < len(self.task_graph.nodes):
            iteration += 1
            
            # apply tasks to queues (processors)
            for qi, proc in enumerate(self.processors):
                if len(self.application[proc.index]) > 0 and queue[qi] == None:
                    task = self.application[proc.index].pop(0)
                    queue[qi] = ProcessingFactory.ScheduledTask(self.parser, proc, task)
                    logging.debug("queue: ", qi, " -> ", task)
                    cost += queue[qi].getCost()
            
            # calculates min time after which something will happen to move clock
            min_construction_time = min(queue, key=lambda x: x.getTime() if x else MAX).getTime()
            min_time = min_construction_time

            for queue_index, queue_el in enumerate(queue):
                # if queue empty, not interesting
                if not queue_el:
                    continue
                parents = self.task_graph.find_parents(queue_el.task)
                logging.debug(queue_el.task, parents)

                # if node has no parents, can be built
                if not parents:
                    queue_el.enable()
                    queue_el.passTime(min_time)
                    

                # all parents have to be constructed
                if parents and set(parents).intersection(set(self.done_tasks)) == set(parents) and len(self.done_tasks) > 0:
                    logging.debug("transfer needed")
                     
                    transfer_time = 0
                    # Resources from all parents have to be on this node to start construction.
                    # Performs transfer logic with additional time required for that.
                    all_here = True
                    for parent in parents:
                        ind = self.done_tasks.index(parent)
                        if self.location[ind] != queue_index and ind in self.done_tasks:
                            all_here = False
                            transfer_time += self.task_graph.get_weight(parent, queue_el.task) / self.transfer[self.location[ind]][queue_index].throughput
                            logging.debug("transfering:", self.location[ind], ind, " -> ", queue_index, ind)
                            self.location[ind] = queue_index
                    
                    # If item can be bult enables it in queue with one step delay (to avoid passing time of transmission)
                    queue_el.enable(True)
                    
                    # If all items are already waiting on current node, construction can be started
                    if all_here:
                        logging.debug("all resources in place!")
                        queue_el.enable()
                    
                    # If there was transfer move time according to time required by transfer, else
                    # move time according to minimal construction time
                    if queue_el and transfer_time > 0:
                        min_time = transfer_time
                    elif queue_el:
                        min_time = min_construction_time
                        
            # Pass time for each element in queue
            for queue_el in queue:
                if queue_el:
                    queue_el.passTime(min_time)

            time += min_time
            logging.info("TIME:", time, min_time, iteration, self.done_tasks)

            # Memory of left times in round buffer to avoid looping for infinity for impossible graphs
            sums[iteration%len(sums)] = sum([x.getTime() for x in queue if x])
            
            # If construction time has passed, item is constructed
            for i, e in enumerate(queue):
                if queue[i] != None and queue[i].getTime() <= 0:
                    # Done has task which were finished, location has nodes on which resources are currently stored
                    self.done_tasks.append(queue[i].task)
                    self.location.append(i)
                    queue[i] = None

            logging.debug(sums)
            # Checks if all average value of sums is equal to last element, 
            # if yes output MAX, MAX which means that it cannot be performed in finite time.
            if sum(sums)/len(sums) == sums[-1]:
                return MAX, MAX
        return time, cost

if __name__ == "__main__":
    parser = Parser("grafy/graph_10_2.txt")
    parser.parse()

    o_props = [0.5, 0.2, 0.1, 0.1, 0.1]
    c_props = [0.5, 0.25, 0.25]
    Procedures(parser, o_props, c_props)

    dg = DecisionGraph()
    pr = Procedures.instance

    dg.add_real_node(DecisionNode(0, 1.0, pr.find_operation_3, pr.find_comm_3))
    dg.add_real_node(DecisionNode(1, 0.3, pr.find_operation_3, pr.find_comm_3))
    dg.add_real_node(DecisionNode(2, 0.2, pr.find_operation_3, pr.find_comm_3))
    dg.add_real_node(DecisionNode(3, 0.5, pr.find_operation_3, pr.find_comm_3))
    dg.add_connection(0, 1, 0)
    dg.add_connection(1, 2, 0)
    dg.add_connection(0, 3, 0)

    pf = ProcessingFactory(parser)
    print(pf.apply(dg))
        
