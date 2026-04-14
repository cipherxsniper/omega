import time
import random
from collections import defaultdict, deque

class OmegaAdaptiveConvergenceV14:
    def __init__(self, brains):
        self.brains = brains
        self.scores = {b: 1.0 for b in brains}
        self.memory = deque(maxlen=5000)
        self.iteration = 0

    def store_memory(self, data):
        self.memory.append({
            "data": data,
            "ts": time.time()
        })

    def memory_bias(self):
        bias = defaultdict(float)

        for item in list(self.memory)[-100:]:
            d = item["data"]
            if isinstance(d, dict) and "brain" in d:
                bias[d["brain"]] += d.get("reward", 0.1)

        return bias

    def step(self):
        self.iteration += 1
        bias = self.memory_bias()

        updates = {}

        for b in self.brains:
            noise = random.uniform(-0.02, 0.02)
            updates[b] = self.scores[b] + bias[b] * 0.1 + noise

        best = max(updates, key=updates.get)
        best_score = updates[best]

        for b in updates:
            if b != best:
                updates[b] += (best_score - updates[b]) * 0.03

        self.scores = updates

        for b, s in updates.items():
            self.store_memory({"brain": b, "reward": s})

        return {
            "top": best,
            "scores": self.scores
        }
