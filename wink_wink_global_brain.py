import json
import time
import os
from collections import defaultdict, deque

MEMORY_FILE = "wink_wink_global_memory.json"

# =========================
# PERSISTENT MEMORY LOAD
# =========================

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "events": [],
            "state_weights": defaultdict(float),
            "transition_graph": defaultdict(float)
        }

    with open(MEMORY_FILE, "r") as f:
        data = json.load(f)

    data["state_weights"] = defaultdict(float, data.get("state_weights", {}))
    data["transition_graph"] = defaultdict(float, data.get("transition_graph", {}))

    return data


def save_memory(mem):
    serializable = {
        "events": mem["events"][-200:],
        "state_weights": dict(mem["state_weights"]),
        "transition_graph": dict(mem["transition_graph"])
    }

    with open(MEMORY_FILE, "w") as f:
        json.dump(serializable, f, indent=2)

# =========================
# GLOBAL EVENT BUS
# =========================

class GlobalBrain:
    def __init__(self):
        self.memory = load_memory()

    def publish(self, source, state, signal, message):
        event = {
            "source": source,
            "state": state,
            "signal": signal,
            "message": message,
            "t": time.time()
        }

        self.memory["events"].append(event)

        # learning update
        self.memory["state_weights"][state] += signal

        # transition learning
        if len(self.memory["events"]) > 1:
            prev = self.memory["events"][-2]["state"]
            curr = state
            self.memory["transition_graph"][(prev, curr)] += 1

        save_memory(self.memory)

    def read_recent(self, n=5):
        return self.memory["events"][-n:]

    def get_state_bias(self):
        return dict(self.memory["state_weights"])


GLOBAL_BRAIN = GlobalBrain()
