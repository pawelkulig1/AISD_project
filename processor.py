
class Processor:
    count = 0

    def __init__(self, index: int, cost: int, limit: int, universal: bool) -> None:
        self.index = index
        self.cost = cost
        self.limit = limit
        self.universal = universal
        
        if (Processor.count > self.limit) and not(self.limit == 0):
            raise ValueError("Processor constructor, cannot initialize another Processor: {}, with cost: {}".format(self.index, self.cost))
        
        Processor.count += 1

    def __str__(self):
        return "id:"+str(self.index)+" cost: "+str(self.cost)+" limit: "+str(self.limit)+" universal: "+str(self.universal)


    def __del__(self) -> None:
        Processor.count -= 1