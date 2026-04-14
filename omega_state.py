import json
import os
import time

STATE_FILE = "omega_global_state.json"


class OmegaState:
    """
    SINGLE SOURCE OF TRUTH
    (V27 Global Brain State)
    """

    def __init__(self):
        self.state = {
            "identity": "OMEGA",
            "version": 27,

            "tick": 0,

            "memory": [],
            "goals": [],
            "events": [],

            "attention": {
                "budget": 3,
                "focus": None
            },

            "swarm": {
                "nodes": 1,
                "status": "online"
            },

            "ml": {
                "reward": 0.0,
                "loss": 0.0
            },

            "stability": 1.0,
            "last_update": time.time()
        }

        self.load()

    # =========================
    # LOAD STATE
    # =========================
    def load(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r") as f:
                    self.state = json.load(f)
            except:
                pass

    # =========================
    # SAVE STATE (SAFE WRITE)
    # =========================
    def save(self):
        self.state["last_update"] = time.time()

        tmp = STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f, indent=2)

        os.replace(tmp, STATE_FILE)

    # =========================
    # UPDATE TICK
    # =========================
    def tick(self):
        self.state["tick"] += 1
        return self.state["tick"]

    # =========================
    # EVENT LOGGING
    # =========================
    def push_event(self, event):
        self.state["events"].append(event)

        if len(self.state["events"]) > 100:
            self.state["events"].pop(0)

    # =========================
    # MEMORY LOGGING
    # =========================
    def remember(self, item):
        self.state["memory"].append(item)

        if len(self.state["memory"]) > 200:
            self.state["memory"].pop(0)

    # =========================
    # SIMPLE ACCESSORS
    # =========================
    def get(self, key, default=None):
        return self.state.get(key, default)

    def set(self, key, value):
        self.state[key] = value


# =========================
# DEBUG RUN
# =========================
if __name__ == "__main__":
    s = OmegaState()

    for i in range(5):
        t = s.tick()
        s.push_event({"type": "heartbeat", "tick": t})
        s.remember(f"tick_{t}")

        s.save()
        print("[OMEGA STATE] tick", t)
        time.sleep(1)
