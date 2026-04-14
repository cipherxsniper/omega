import json
import os
import time

class CRDTGraphV5:
    def __init__(self, path="omega_crdt_v5.json"):
        self.path = path
        self.state = self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)

        return {
            "nodes": {},
            "ideas": {},
            "meta": {"version": 5}
        }

    def merge(self, incoming):
        # 🧠 CRDT RULE: last-write-wins + strength merge
        for k, v in incoming.get("ideas", {}).items():
            if k not in self.state["ideas"]:
                self.state["ideas"][k] = v
            else:
                self.state["ideas"][k]["strength"] = (
                    self.state["ideas"][k]["strength"] + v.get("strength", 0)
                ) / 2

        for k, v in incoming.get("nodes", {}).items():
            self.state["nodes"][k] = v

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.state, f, indent=2)
