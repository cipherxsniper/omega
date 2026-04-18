# 🧠 Omega v17 Global State (Graph + Memory Backbone)

import json
import os

STATE_FILE = "omega_state_v17.json"

def load():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE))
    return {
        "nodes": {},
        "clusters": {},
        "global_energy": 1.0,
        "step": 0
    }

def save(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

class GlobalState:
    def __init__(self):
        self.state = load()

    def get_node(self, node):
        if node not in self.state["nodes"]:
            self.state["nodes"][node] = {
                "energy": 0.5,
                "trust": 0.5,
                "stability": 0.5,
                "memory": [],
                "cluster": None
            }
        return self.state["nodes"][node]

    def update(self):
        self.state["step"] += 1
        save(self.state)
