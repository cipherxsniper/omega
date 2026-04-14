import math
import random
import time


class OmegaAdaptiveConvergenceV15:
    def __init__(self, brains):
        self.brains = brains

        # core scoring system
        self.scores = {b: 1.0 for b in brains}
        self.step_count = 0

        # MEMORY FUSION LAYER
        self.memory = []
        self.brain_memory = {b: [] for b in brains}

        # dynamics
        self.decay = 0.90
        self.noise = 0.03
        self.memory_influence = 0.15
        self.max_cap = 1e6

    # -------------------------
    # MEMORY CORE
    # -------------------------
    def store_memory(self, event):
        self.memory.append({
            "event": event,
            "ts": time.time()
        })

        if len(self.memory) > 200:
            self.memory = self.memory[-200:]

    def brain_memory_update(self, brain, value):
        self.brain_memory[brain].append(value)

        if len(self.brain_memory[brain]) > 50:
            self.brain_memory[brain] = self.brain_memory[brain][-50:]

    def memory_bias(self, brain):
        history = self.brain_memory[brain]
        if not history:
            return 1.0
        return sum(history) / len(history)

    # -------------------------
    # STABILITY CORE
    # -------------------------
    def stabilize(self, val):
        if val > self.max_cap:
            val = math.log(val + 1)
        if val < 1e-9:
            val = 1e-9
        return val

    def normalize(self):
        total = sum(self.scores.values())
        if total == 0:
            return
        for k in self.scores:
            self.scores[k] /= total

    # -------------------------
    # MAIN STEP
    # -------------------------
    def step(self):
        self.step_count += 1
        new_scores = {}

        global_signal = sum(self.scores.values()) / len(self.scores)

        for b in self.brains:
            noise = random.random() * self.noise
            mem_bias = self.memory_bias(b)
            current = self.scores[b]

            growth = (
                current
                * (1 + noise)
                * self.decay
                * (1 + self.memory_influence * mem_bias)
                * (1 + 0.05 * global_signal)
            )

            stabilized = self.stabilize(growth)
            new_scores[b] = stabilized

            self.brain_memory_update(b, stabilized)

        self.scores = new_scores
        self.normalize()

        top = max(self.scores, key=self.scores.get)

        self.store_memory({
            "step": self.step_count,
            "top": top,
            "scores": dict(self.scores)
        })

        return {
            "step": self.step_count,
            "top": top,
            "scores": self.scores,
            "memory_size": len(self.memory)
        }
