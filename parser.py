from processor import Processor
from task_graph import TaskGraph
from channel import Channel

class Parser:
    def __init__(self, filename: str) -> None:
        """ _filename: str - name of graph file to load
            tasks_count: int - number of tasks (@tasks n)
            proc_count: int - number of processing units (@proc n)
            comms_count: int - number of channeling units (@comm n)
            times: [[], [], ..., []] - 2D list with times. For example times[1][3] -> task1 on machine3.
            costs: [[], [], ..., []] - 2D list with costs. For example costs[1][3] -> task1 on machine3.
            comms: [] - 1D list containing objects representing connection (Channel)
            procs: [] - 1D list containing objects representing processors (Processor)
            graph: Graph - graph object 
        """
        self._filename = filename
        self.tasks_count = 0
        self.proc_count = 0
        self.comms_count = 0
        self.times = []
        self.costs = []
        self.comms = []
        self.procs = []
        self.graph = TaskGraph()

    def parse(self):
        with open(self._filename, "r") as f: #Reading file line by line
            data = f.readline()

            while (data != ""):
                data = data.split();
                
                if(data[0] == "@tasks"):    #Parsing graph data for Graph object
                    self.tasks_count = int(data[1])
                    for i in range(self.tasks_count):   #Nodes adding
                        self.graph.add_node(i)
                    for i in range(self.tasks_count):   #Connections adding
                        data = f.readline().split()
                        number_of_neighbours = int(data[1])
                        for j in range(2,number_of_neighbours+2):
                            
                            neighbour_and_weight = data[j].split('(')

                            node = i
                            neighbour = int(neighbour_and_weight[0])
                            weight = float(neighbour_and_weight[1].replace(')',''))
                            self.graph.add_connection( node, neighbour, weight)
                            """ print("Node nr: ",node," ma sasiada: ",neighbour," waga: ", weight ) """

                elif(data[0] == "@proc"):   #Parsing processors data to procs list with Processor objects
                    self.proc_count = int(data[1])

                    for i in range(self.proc_count):
                        data = f.readline().split()

                        index = i
                        cost = float(data[0])
                        limit = int(data[1])
                        universal = True if (int(data[2]) == 1) else False
                        self.procs.append( Processor( index, cost, limit, universal) )
                        """ print(self.procs[i]) """

                elif(data[0] == "@times"):   #Parsing times to times array
                    for i in range(self.tasks_count):
                        data = f.readline().split()
                        data[:] = [float(x) for x in data] #converting to float
                        self.times.append(data)
                    """ print(self.times) """

                elif(data[0] == "@cost"):   #Parsing cost to cost array
                    for i in range(self.tasks_count):
                        data = f.readline().split()
                        data[:] = [float(x) for x in data] #converting to float
                        self.costs.append(data)
                    """ print(self.costs) """

                elif(data[0] == "@comm"):   #Parsing channels data to comms list with Channel objects
                    self.comms_count = int(data[1])
                    for i in range(self.comms_count):
                        data = f.readline()
                        self.comms.append( Channel(data) )
                        """ print(self.comms[i]) """

                else:
                    raise ValueError('Wrong data format!')
                data = f.readline()
            
if __name__ == "__main__":
    parser = Parser("grafy/graph_10_2.txt")
    parser.parse()
    
