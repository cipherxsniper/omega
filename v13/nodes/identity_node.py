import uuid
import math

class IdentityNode:
    def __init__(self, x, y):
        self.id = str(uuid.uuid4())

        # position
        self.x = x
        self.y = y

        # aggregate signals
        self.strength = 0.0
        self.members = 0

        # STATE VECTOR (CORE UPGRADE)
        self.state = {
            "activation": 0.0,
            "stability": 0.0,
            "coherence": 0.0,
            "momentum": 0.0,
            "entropy": 0.0
        }

        # memory trace
        self.history = []
        self.age = 0

    def integrate(self, event):
        s = event["strength"]

        self.strength += s
        self.members += 1

        # state vector updates
        self.state["activation"] += s * 0.2
        self.state["coherence"] += 0.05
        self.state["stability"] += 0.01
        self.state["entropy"] *= 0.98

        dx = event["x"] - self.x
        dy = event["y"] - self.y

        self.state["momentum"] += math.sqrt(dx*dx + dy*dy) * 0.001

        self.history.append(s)

    def decay(self):
        self.state["activation"] *= 0.95
        self.state["entropy"] += 0.01
        self.state["entropy"] -= self.state["stability"] * 0.02

        self.state["entropy"] = max(0, min(1, self.state["entropy"]))
        self.state["activation"] = max(0, min(1, self.state["activation"]))

        self.age += 1

    def is_dead(self):
        return self.state["activation"] < 0.02 and self.members < 2
