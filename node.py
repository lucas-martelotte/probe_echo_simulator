from config import ADJACENCY_LIST_PATH

class Node():
    def __init__(self, process_id):

        self.adjacency = None
        with open(ADJACENCY_LIST_PATH) as f:
            self.adjacency = [int(i) for i in \
                              f.readlines()[process_id-1].replace("\n","").split(" ")]

        self.process_id        = process_id
        self.father_process_id = 0

        self.children          = []
        self.partial_output    = []
        self.final_output      = 0

        self.probe             = False
        self.initial_node      = False

    def reset(self):

        with open(ADJACENCY_LIST_PATH) as f:
            self.adjacency = [int(i) for i in \
                              f.readlines()[self.process_id-1].replace("\n","").split(" ")]

        self.father_process_id = 0

        self.children          = []
        self.partial_output    = []
        self.final_output      = 0

        self.probe             = False
        self.inicial           = False
