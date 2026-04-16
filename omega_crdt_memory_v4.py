import json
import os
import time

class OmegaCRDTMemoryV4:
    def __init__(self, path="omega_crdt_v4.json"):
        self.path = path
        self.state = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {
            "nodes": {},
            "ideas": {},
            "events": []
        }

    def merge(self, incoming):
        for k in incoming.get("nodes", {}):
            self.state["nodes"][k] = incoming["nodes"][k]

        for k in incoming.get("ideas", {}):
            self.state["ideas"][k] = incoming["ideas"][k]

        self.state["events"].append({
            "t": time.time(),
            "data": incoming
        })

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)
