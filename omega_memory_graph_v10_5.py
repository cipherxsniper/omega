# 🧠 Omega v10.5 Memory Graph Engine
# Cross-node shared memory + causal learning

import json
import os
import time
from collections import defaultdict

STATE_FILE = "omega_memory_graph_v10_5.json"

class MemoryGraph:

    def __init__(self):
        self.state = self.load()

        # graph structure
        self.nodes = self.state.get("nodes", {})
        self.edges = self.state.get("edges", defaultdict(dict))

    def load(self):
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        return {"nodes": {}, "edges": {}}

    def save(self):
        with open(STATE_FILE, "w") as f:
            json.dump({
                "nodes": self.nodes,
                "edges": self.edges
            }, f, indent=2)

    # 🧠 register node memory
    def register(self, node):
        if node not in self.nodes:
            self.nodes[node] = {
                "memory": [],
                "strength": 0.5,
                "activation": 0.5
            }

    # 🧠 write shared memory event
    def write(self, node, event, score, decision):
        self.register(node)

        entry = {
            "event": event,
            "score": score,
            "decision": decision,
            "timestamp": time.time()
        }

        self.nodes[node]["memory"].append(entry)

        # limit memory size
        self.nodes[node]["memory"] = self.nodes[node]["memory"][-50:]

        self.propagate(node, score, decision)

        self.save()

    # 🧠 cross-node propagation (CORE FEATURE)
    def propagate(self, source, score, decision):

        influence = (score - 0.5)

        for target in self.nodes:

            if target == source:
                continue

            self.edges.setdefault(source, {})
            self.edges[source][target] = self.edges[source].get(target, 0.1)

            # update edge strength
            self.edges[source][target] += influence * 0.05
            self.edges[source][target] = max(0.01, min(1.0, self.edges[source][target]))

            # inject memory influence
            self.nodes[target]["activation"] += influence * 0.02
            self.nodes[target]["activation"] = max(0.01, min(1.0, self.nodes[target]["activation"]))

    # 🧠 read contextual memory
    def read(self, node):
        self.register(node)

        return {
            "self_memory": self.nodes[node]["memory"][-10:],
            "activation": self.nodes[node]["activation"],
            "connections": self.edges.get(node, {})
        }
