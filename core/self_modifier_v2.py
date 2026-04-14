# core/self_modifier_v2.py

import time
import os

class SelfModifier:
    def __init__(self):
        self.last = 0

    def evolve(self):
        now = time.time()
        if now - self.last < 60:
            return "Cooldown active"

        self.last = now

        path = "./brains/evolved_brain.py"
        with open(path, "w") as f:
            f.write(f"# evolved at {now}\n")

        return "Brain evolved"
