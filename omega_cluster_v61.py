import random
import math

class ClusterEngineV61:
    def __init__(self, state):
        self.state = state

    def similarity(self, a, b):
        # simple structural similarity heuristic
        sa = self.state["ideas"][a].get("strength", 1)
        sb = self.state["ideas"][b].get("strength", 1)

        # closer strength = higher similarity
        return 1.0 / (1.0 + abs(sa - sb))

    def merge(self, a, b):
        ia = self.state["ideas"][a]
        ib = self.state["ideas"][b]

        # 🌌 gravity fusion
        new_strength = (ia["strength"] + ib["strength"]) / 2

        ia["strength"] = new_strength
        ia["links"] = list(set(ia.get("links", []) + ib.get("links", [])))

        # remove weaker node
        del self.state["ideas"][b]

    def step(self):
        ideas = list(self.state["ideas"].keys())

        if len(ideas) < 2:
            return

        # pick candidates
        for _ in range(min(3, len(ideas))):
            a, b = random.sample(ideas, 2)

            if a not in self.state["ideas"] or b not in self.state["ideas"]:
                continue

            sim = self.similarity(a, b)

            # 🧲 merge threshold
            if sim > 0.85:
                self.merge(a, b)
                break
