import json
import os

class IdentityGraph:
    def __init__(self, path="omega_identity_graph_v2.json"):
        self.path = path
        self.graph = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {"nodes": {}, "edges": []}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.graph, f, indent=2)

    def update_node(self, node_id, data):
        self.graph["nodes"][node_id] = data

    def link(self, a, b, weight=0.1):
        self.graph["edges"].append({
            "a": a,
            "b": b,
            "weight": weight
        })
