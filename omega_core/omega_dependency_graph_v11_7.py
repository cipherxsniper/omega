# 🧠 Omega v11.7 Dependency Flow Engine (Directional Cognition)

import random
import time
from collections import defaultdict

class DependencyGraph:

    def __init__(self):

        # directed weighted edges: A -> B
        self.edges = defaultdict(lambda: defaultdict(float))

        self.nodes = [
            "node_attention",
            "node_goal",
            "node_memory",
            "node_stability"
        ]

        # initialize base cognitive structure
        self._init_graph()

        self.flow_history = []

    def _init_graph(self):

        # base cognitive architecture (human-like loop)
        self.connect("node_attention", "node_goal", 0.7)
        self.connect("node_goal", "node_memory", 0.6)
        self.connect("node_memory", "node_stability", 0.5)
        self.connect("node_stability", "node_attention", 0.4)

        # cross-links (emergent cognition paths)
        self.connect("node_attention", "node_memory", 0.3)
        self.connect("node_goal", "node_attention", 0.2)

    def connect(self, a, b, weight):

        self.edges[a][b] = weight

    def propagate(self, activations):

        new_state = defaultdict(float)
        flow_events = []

        for src in activations:

            for dst, weight in self.edges[src].items():

                signal = activations[src] * weight

                # noise prevents collapse into static graph
                noise = random.uniform(-0.02, 0.02)

                signal = max(0.0, signal + noise)

                new_state[dst] += signal

                flow_events.append((src, dst, round(signal, 3)))

        self.flow_history.append(flow_events[-10:])

        return dict(new_state)

    def get_edges(self):

        return self.edges

    def get_recent_flows(self):

        return self.flow_history[-1] if self.flow_history else []
