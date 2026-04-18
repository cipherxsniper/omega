class SharedMemory:

    def __init__(self):
        self.graph = {}
        self.beliefs = {}
        self.history = []

    def update_belief(self, key, value):

        self.beliefs[key] = value
        self.history.append((key, value))

    def link_nodes(self, a, b):

        if a not in self.graph:
            self.graph[a] = []

        self.graph[a].append(b)
