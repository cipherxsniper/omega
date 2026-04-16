import random

class OmegaEmergentGraphV74:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.node_score = {}
        self.age = {}

    def register(self, name, fn):
        self.nodes[name] = fn
        self.edges.setdefault(name, {})
        self.node_score[name] = 1.0
        self.age[name] = 0

    def connect(self, a, b, w=0.5):
        self.edges[a][b] = w

    def decay_edges(self):
        for a in list(self.edges.keys()):
            for b in list(self.edges[a].keys()):
                self.edges[a][b] *= 0.98

                if self.edges[a][b] < 0.1:
                    del self.edges[a][b]

    def reinforce(self, a, b, success):
        if b not in self.edges[a]:
            self.edges[a][b] = 0.5

        if success:
            self.edges[a][b] = min(1.0, self.edges[a][b] + 0.05)
        else:
            self.edges[a][b] = max(0.05, self.edges[a][b] - 0.03)

    def maybe_create_edge(self, a, b):
        if b not in self.edges[a]:
            if random.random() < 0.02:
                self.edges[a][b] = 0.3

    def update_node_score(self, node, health):
        self.node_score[node] = (
            self.node_score[node] * 0.9 + health * 0.1
        )
