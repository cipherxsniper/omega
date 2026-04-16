import random
import math

class GravityEngineV6:
    def __init__(self, state):
        self.state = state

    def apply_gravity(self):
        ideas = self.state["ideas"]

        keys = list(ideas.keys())

        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]

                ia = ideas[a]
                ib = ideas[b]

                sa = ia.get("strength", 1.0)
                sb = ib.get("strength", 1.0)

                # 🌌 cognitive attraction force
                force = (sa * sb) * 0.01

                # merge influence slightly
                ia["strength"] += force * random.uniform(0.0, 0.2)
                ib["strength"] += force * random.uniform(0.0, 0.2)
