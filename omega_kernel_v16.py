import json
import time
import os
import random

BUS_FILE = "omega_cognition_bus.json"


# -----------------------------
# COGNITION BUS (SINGLE SOURCE OF TRUTH)
# -----------------------------
class CognitionBus:
    def __init__(self):
        self.state = {
            "beliefs": [],
            "messages": [],
            "global_attention": 1.0,
            "global_reward": 1.0,
            "tick": 0
        }
        self.load()

    def load(self):
        if os.path.exists(BUS_FILE):
            try:
                with open(BUS_FILE, "r") as f:
                    self.state = json.load(f)
            except:
                pass

    def save(self):
        tmp = BUS_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(self.state, f, indent=2)
        os.replace(tmp, BUS_FILE)

    def send(self, msg):
        self.state["messages"].append(msg)
        self.state["messages"] = self.state["messages"][-50:]

    def read_messages(self, source=None):
        msgs = self.state["messages"]
        if source:
            return [m for m in msgs if m.get("from") == source]
        return msgs


# -----------------------------
# MODULE WRAPPER
# -----------------------------
class Module:
    def __init__(self, name, bus):
        self.name = name
        self.bus = bus
        self.bias = random.uniform(-0.1, 0.1)

    def think(self):
        return random.random() + self.bias

    def act(self):
        output = self.think()

        msg = {
            "from": self.name,
            "type": "signal",
            "value": output,
            "time": time.time()
        }

        self.bus.send(msg)


# -----------------------------
# CONSENSUS ENGINE
# -----------------------------
def consensus(bus):
    msgs = bus.read_messages()

    if not msgs:
        return 1.0

    values = [m["value"] for m in msgs if "value" in m]

    if not values:
        return 1.0

    # weighted cognitive average
    return sum(values) / len(values)


# -----------------------------
# KERNEL V16
# -----------------------------
class OmegaV16:
    def __init__(self):
        self.bus = CognitionBus()

        self.modules = [
            Module("ml", self.bus),
            Module("swarm", self.bus),
            Module("memory", self.bus)
        ]

    def step(self):
        self.bus.state["tick"] += 1

        # modules act
        for m in self.modules:
            m.act()

        # global decision
        decision = consensus(self.bus)

        # update global cognition
        self.bus.state["global_attention"] = decision
        self.bus.state["global_reward"] = decision * random.uniform(0.95, 1.05)

        self.bus.save()

        print(
            f"[V16] tick {self.bus.state['tick']} | "
            f"consensus={decision:.3f} | "
            f"messages={len(self.bus.state['messages'])}"
        )

    def run(self):
        print("[V16] DISTRIBUTED COGNITION BUS ONLINE")

        while True:
            self.step()
            time.sleep(2)


if __name__ == "__main__":
    OmegaV16().run()
