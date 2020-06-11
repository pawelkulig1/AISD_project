
class Processor:
    """Opis"""
    count = 0
    def __init__(self, index: int, cost: float, limit: int, universal: bool) -> None:
        """
            Processor is a class that contains informations about single Processor object.

            Parameters
            ----------
            index: int
            cost: float
            limit: int
                Values: 0 - declares infinity amount, 1 and more - is exact amount
            universal: bool

            Returns
            ----------
            None
        """
        self.index = index
        self.cost = cost
        self.limit = limit
        self.universal = universal
        
        if (Processor.count > self.limit) and not(self.limit == 0):
            raise ValueError("Processor constructor, cannot initialize another Processor: {}, with cost: {}".format(self.index, self.cost))
        
        Processor.count += 1

    def __str__(self):
        """
            Function __str__() provides ability to display Processor object's informations by print() function.

            Parameters
            ----------
            None

            Returns
            ----------
            Str
        """
        return "id:"+str(self.index)+" cost: "+str(self.cost)+" limit: "+str(self.limit)+" universal: "+str(self.universal)


    def __del__(self) -> None:
        """
            Function __del__() is Processor's destructor.

            Parameters
            ----------
            None

            Returns
            ----------
            None
        """
        Processor.count -= 1
