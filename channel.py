from processor import Processor

class Channel:
    def __init__(self, line: str) -> None:
        """ Gets line of CHANN in constructor and constructs object that will be used later
            transmission = [] bool values (True/False)
        """
        self.line = line
        self.id = 0
        self.transmission = []
        self.cost = 0
        self.throughput = 0
        self.parse(line)
    
    def parse(self,line) -> None:
        data = self.line.split()
        self.id = int(str(data[0]).replace("CHAN",''))
        self.cost = float(data[1])
        self.throughput = float(data[2])
        for x in range(3,len(data)):
            self.transmission.append( bool(data))

    def can_connect(self, processor: Processor) -> bool:
        return self.transmission[ processor.id ]

    def get_cost(self) -> int:
        return self.cost

    def get_throughput(self) -> int:
        return self.throughput

    def __str__(self):
        return "id: "+str(self.id)+" transmission: "+str(self.transmission)+" cost: "+str(self.cost)+" troughput: "+str(self.throughput)
