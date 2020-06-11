import logging
from collections import Counter
from parser import Parser
import random

MAX = 1e10

class Procedures:
    instance = None #singleton - sort of

    def __init__(self, parser: Parser, oper_props: list, comm_props: list) -> None:
        self.last_operator = self.find_operation_1
        self.parser = parser
        
        self.oper_props = oper_props
        assert len(self.oper_props) == 5

        self.comm_props = comm_props
        assert len(self.comm_props) == 3

        self.check_prop(self.oper_props)
        self.check_prop(self.comm_props)

        self.application = None

        Procedures.instance = self
    
    def check_prop(self, prop):
        assert sum(prop) > 0.99 and sum(prop) < 1.01

    def get_oper(self):
        return random.choices([ \
            self.find_operation_1, \
            self.find_operation_2, \
            self.find_operation_3, \
            self.find_operation_4, \
            self.find_operation_5], self.oper_props, k=1)[0]

    def get_comm(self):
        return random.choices([self.find_comm_1, self.find_comm_2, self.find_comm_3], self.comm_props, k=1)[0]

    def set_application(self, application) -> None:
        self.application = application

    def find_operation_1(self, task):
            self.last_operator = self.find_operation_1
            return self.parser.costs[task][:].index(min(self.parser.costs[task][:]))

    def find_operation_2(self, task):
        self.last_operator = self.find_operation_2
        return self.parser.times[task][:].index(min(self.parser.times[task][:]))

    def find_operation_3(self, task):
        min_val = MAX
        min_ind = -1
        for i, p in enumerate(self.parser.procs):
            val = self.parser.times[task][i] * self.parser.costs[task][i]
            if val < min_val:
                min_val = val
                min_ind = i

        self.last_operator = self.find_operation_3
        assert min_ind != -1
        return min_ind

    def find_operation_4(self, task):
        return self.last_operator(task)

    def find_operation_5(self, task):
        min_l = MAX
        min_ind = -1
        for i, key in enumerate(self.application.keys()):
            temp = len(self.application[key])
            if temp < min_l:
                min_l = temp
                min_ind = i

        self.last_operator = self.find_operation_5
        assert min_ind != -1
        return min_ind

    def find_comm_1(self, transfer=None):
        logging.info("find_commm_1")     
        return self.parser.comms.index(min(self.parser.comms, key=lambda x: x.get_cost()))

    def find_comm_2(self, transfer=None):
        logging.info("find_commm_2")
        return self.parser.comms.index(max(self.parser.comms, key=lambda x: x.get_throughput()))

    def find_comm_3(self, transfer=None):
        logging.info("find_commm_3")
        flat_list = [i for sub in transfer for i in sub]
        r = Counter([x.id for x in flat_list if x]).most_common(1)[0][0]
        return r