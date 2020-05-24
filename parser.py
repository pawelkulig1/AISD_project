from processor import Processor

class Parser:
    def __init__(self, filename: str) -> None:
        """ _filename: str - name of graph file to load
            tasks_count: int - number of tasks (@tasks n)
            proc_count: int - number of processing units (@proc n)
            times: [[], [], ..., []] - 2D list with times. For example times[1][3] -> task1 on machine3.
            costs: [[], [], ..., []] - 2D list with costs. For example costs[1][3] -> task1 on machine3.
            comms: [] - 1D list containing objects representing connection (Channel)
        """
        self._filename = filename
        self.tasks_count = 0
        self.proc_count = 0
        self.times = []
        self.costs = []
        self.comms = []

    def parse(self):
        with open(self._filename, "r") as f:
            data = f.read.splitlines()
        #TODO
        pass

class Channel:
    def __init__(self, line: str) -> None:
        """ Gets line of CHANn in constructor and constructs object that will be used later

        """
        self.line = line
        self.id = 0
        self.transmission = []
        self.cost = 0
        self.throughput = 0
        self.parse(line)
    
    def parse(self) -> None:
        #use self.line and parse it
        #self.id = ...
        #self.transmission = ...
        #TODO
        pass

    def can_connect(self, processor: Processor) -> bool:
        #TODO
        pass

    def get_cost(self) -> int:
        #TODO
        pass
