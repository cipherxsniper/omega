# 🔁 Omega v11.3 Dependency Flow Engine (Behavioral Graph)

import json
import os
from collections import defaultdict

STATE_FILE = "omega_memory_graph_v10_5.json"


class DependencyGraph:

    def __init__(self):
        self.state = self.load()

        # influence edges: A → B weight
        self.edges = defaultdict(lambda: defaultdict(float))

    def load(self):
        if os.path.exists(STATE_FILE):
            return json.load(open(STATE_FILE))
        return {"nodes": {}, "global_memory": []}

    def update_from_memory(self):

        memory = self.state.get("global_memory", [])[-200:]

        # build co-occurrence influence graph
        for i in range(len(memory) - 1):

            a = memory[i]["node"]
            b = memory[i + 1]["node"]

            if a != b:
                self.edges[a][b] += 0.1

    def decay(self):

        # prevents infinite growth
        for a in list(self.edges.keys()):
            for b in list(self.edges[a].keys()):
                self.edges[a][b] *= 0.98

    def get_edges(self):
        return self.edges
