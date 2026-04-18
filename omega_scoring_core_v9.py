import json
import os
import random

STATE_FILE = "omega_state_v9_5.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"nodes": {}, "global_step": 0}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

class AdaptiveScoringCore:
    def __init__(self):
        self.state = load_state()

    def get_node(self, name):
        if name not in self.state["nodes"]:
            self.state["nodes"][name] = {
                "weight": 0.5,
                "history": [],
                "stability": 0.5
            }
        return self.state["nodes"][name]

    def compute_score(self, name, input_signal=0.0):
        node = self.get_node(name)

        base = node["weight"]
        stability = node["stability"]

        noise = random.uniform(-0.05, 0.05)
        score = (base * 0.7 + stability * 0.3) + noise + input_signal

        return max(0.0, min(1.0, score))

    def update(self, name, score, result):
        node = self.get_node(name)

        node["history"].append(score)

        if result == "SUCCESS":
            node["weight"] += 0.02
            node["stability"] += 0.01
        elif result == "FAIL":
            node["weight"] -= 0.03
            node["stability"] -= 0.02
        else:
            node["weight"] *= 0.999

        node["weight"] = max(0.01, min(1.0, node["weight"]))
        node["stability"] = max(0.01, min(1.0, node["stability"]))

        self.state["global_step"] += 1
        save_state(self.state)
