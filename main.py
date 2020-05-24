from parser import Parser

class Simulation:
    def __init__(self, parser: Parser, alpha: int, beta: float, gamma: float, delta: float, epsilon: float):
        """ 
            parser: Parser - instance of parser
            alpha: int - user provided parameter
            beta:  float - user provided parameter - modificating number of solutions from selection
            gamma: float - user provided parameter - modificating number of solutions from crossing
            delta: float - user provided parameter - modificating number of solutions from mutation
            epsilon: float - user provided parameter - limit of epochs with no progress
            n :    int - number of tasks in graph
            z :    int - number of processing types
            initial_size: int - number of entities in intial population

        """
        self.parser = parser
        self.alpha = alpha 
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.epsilon = epsilon
        self.n = 0
        self.z = 0
        self.initial_size = 0
        self.max_iters = 1 # TODO - for now



    def run(self) -> None:
        self.create_initial_population()
        for i in range(self.max_iters):
            if self.check_stop_condition:
                break
            self.sort_population()
            self.apply_crossover()
            self.apply_mutation()

    def sort_population(self) -> None:
        # TODO
        pass

    def apply_crossover(self) -> None:
        # TODO
        pass

    def apply_mutation(self) -> None:
        # TODO
        pass

    def check_stop_condition(self) -> bool:
        """ if last epsilon epochs without progress returns true else false"""
        # TODO
        return False 

def main() -> None:
    parser = Parser("graph10_wagi.txt")
    s = Simulation(parser, 20, 0.3, 0.3, 0.3, 5)
    s.run()

if __name__ == "__main__":
    main()