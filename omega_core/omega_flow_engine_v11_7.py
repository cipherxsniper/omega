# 🧠 Omega v11.7 Dependency Flow Engine

import random
from collections import defaultdict

class FlowEngine:

    def __init__(self):
        self.edges = defaultdict(lambda: defaultdict(float))

        # base cognitive wiring
        self.connect("node_attention", "node_goal", 0.35)
        self.connect("node_goal", "node_memory", 0.28)
        self.connect("node_memory", "node_stability", 0.22)
        self.connect("node_stability", "node_attention", 0.18)

    def connect(self, src, dst, weight):
        self.edges[src][dst] = weight

    def propagate(self, field_state):
        updates = defaultdict(float)

        for src, targets in self.edges.items():
            src_value = field_state.get(src, 0.0)

            for dst, w in targets.items():
                noise = random.uniform(-0.01, 0.01)

                influence = src_value * w + noise
                updates[dst] += influence

        return updates

    def get_flows(self):
        return self.edges
