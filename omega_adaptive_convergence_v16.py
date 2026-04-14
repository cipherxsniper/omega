import math
import random
import time
import json
import os
import traceback


class OmegaAdaptiveConvergenceV16:
    def __init__(self, brains):
        self.brains = brains
        self.scores = {b: 1.0 for b in brains}

        # MEMORY SYSTEM
        self.memory = []
        self.brain_memory = {b: [] for b in brains}

        # CORE PARAMETERS (now dynamic)
        self.decay = 0.90
        self.noise = 0.03
        self.memory_influence = 0.15

        # SELF-HEALING SYSTEM
        self.step_count = 0
        self.crash_count = 0
        self.last_reset = time.time()

        # STABILITY THRESHOLDS
        self.divergence_limit = 5.0
        self.stagnation_window = 20

    # -------------------------
    # MEMORY SYSTEM
    # -------------------------
    def store_memory(self, event):
        self.memory.append({
            "event": event,
            "ts": time.time()
        })

        if len(self.memory) > 300:
            self.memory = self.memory[-300:]

    def brain_memory_update(self, b, val):
        self.brain_memory[b].append(val)
        if len(self.brain_memory[b]) > 60:
            self.brain_memory[b] = self.brain_memory[b][-60:]

    def memory_bias(self, b):
        h = self.brain_memory[b]
        return sum(h) / len(h) if h else 1.0

    # -------------------------
    # STABILITY CORE
    # -------------------------
    def instability_score(self):
        vals = list(self.scores.values())
        return max(vals) / (min(vals) + 1e-9)

    def stagnation_detected(self):
        if len(self.memory) < self.stagnation_window:
            return False

        recent = self.memory[-self.stagnation_window:]
        tops = [m["event"]["top"] for m in recent if "top" in m["event"]]

        return len(set(tops)) <= 1

    # -------------------------
    # SELF-HEALING ENGINE
    # -------------------------
    def self_heal(self):
        instability = self.instability_score()

        # TOO CHAOTIC → stabilize
        if instability > self.divergence_limit:
            self.decay = min(0.97, self.decay + 0.01)
            self.noise *= 0.9

        # TOO STABLE → inject exploration
        if self.stagnation_detected():
            self.noise = min(0.08, self.noise + 0.01)
            self.decay = max(0.85, self.decay - 0.005)

        # slow memory drift adaptation
        self.memory_influence = 0.10 + (len(self.memory) / 10000)

    # -------------------------
    # CORE STEP
    # -------------------------
    def step(self):
        try:
            self.step_count += 1

            self.self_heal()

            new_scores = {}
            global_signal = sum(self.scores.values()) / len(self.scores)

            for b in self.brains:
                noise = random.random() * self.noise
                mem = self.memory_bias(b)
                current = self.scores[b]

                growth = (
                    current
                    * (1 + noise)
                    * self.decay
                    * (1 + self.memory_influence * mem)
                    * (1 + 0.05 * global_signal)
                )

                val = max(1e-9, min(growth, 1e6))
                new_scores[b] = val

                self.brain_memory_update(b, val)

            self.scores = self.normalize(new_scores)

            top = max(self.scores, key=self.scores.get)

            self.store_memory({
                "step": self.step_count,
                "top": top,
                "scores": dict(self.scores),
                "instability": self.instability_score()
            })

            return {
                "step": self.step_count,
                "top": top,
                "scores": self.scores,
                "memory": len(self.memory),
                "instability": self.instability_score()
            }

        except Exception as e:
            self.crash_count += 1
            self.store_memory({"error": str(e), "trace": traceback.format_exc()})
            return {"error": str(e)}

    # -------------------------
    # NORMALIZATION
    # -------------------------
    def normalize(self, scores):
        total = sum(scores.values())
        if total == 0:
            return scores
        return {k: v / total for k, v in scores.items()}
