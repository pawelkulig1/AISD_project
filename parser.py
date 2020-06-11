from processor import Processor
from task_graph import TaskGraph
from channel import Channel

class Parser:
    instance = None

    def __init__(self, filename: str) -> None:
        """ 
            Parser is a class that provides converting data from text file
            to structures such as Graph, Channels, Processors, Tables of times and costs
            and hold them for later use.

            Parameters
            ----------
            filename: str
                Name of graph file to load

            Returns
            ----------
            None
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
        Parser.instance = self

    def parse(self):
        """ 
            Parse() is method that initiates processing data from text file
            to internal structures in Parser object. Parser creates graph - TaskGraph() - with verticies, edges and weights,
            procs[]- table with Processors, comms[] - table with Channels, times[] - table with times, costs[] - table with costs,
            counts amounts of:  tasks - tasks_count, processors - proc_count and channels - comms_count. 

            Parameters
            ----------
            None

            Returns
            ----------
            None
        """
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
    
