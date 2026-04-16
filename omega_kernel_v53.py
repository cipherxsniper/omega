# OMEGA KERNEL V53 — COGNITIVE EQUILIBRIUM SYSTEM

import random
import math
import time

class OmegaV53:

    def __init__(self):
        self.tick = 0

        # Core system state
        self.entropy = 0.3
        self.temp = 1.3
        self.nodes = 10

        # Targets
        self.TARGET_ENTROPY = 0.35
        self.MIN_ENTROPY = 0.25
        self.MAX_ENTROPY = 0.45

        self.MAX_NODES = 100

        # Learning memory
        self.history = []

        print("[V53] COGNITIVE EQUILIBRIUM SYSTEM ONLINE")

    # ----------------------------
    # Core Loop
    # ----------------------------

    def step(self):
        self.tick += 1

        # Simulated signal input
        signal = random.uniform(-1, 1)

        # Update entropy based on signal + system complexity
        self.entropy += signal * 0.05
        self.entropy += (self.nodes / 1000)

        # Clamp entropy
        self.entropy = self.clamp(self.entropy, 0.0, 1.0)

        # ----------------------------
        # EQUILIBRIUM CONTROL
        # ----------------------------

        drift = self.entropy - self.TARGET_ENTROPY

        # Pull entropy toward equilibrium
        self.entropy -= drift * 0.1

        # Adjust temperature dynamically
        if self.entropy > self.MAX_ENTROPY:
            self.temp *= 0.95
        elif self.entropy < self.MIN_ENTROPY:
            self.temp *= 1.05

        # Stabilize temperature
        self.temp = self.clamp(self.temp, 0.5, 2.0)

        # ----------------------------
        # NODE EVOLUTION
        # ----------------------------

        if self.entropy > 0.3:
            growth = int(self.temp * random.uniform(0.5, 2))
            self.nodes += growth

        # Node pruning (critical)
        if self.nodes > self.MAX_NODES:
            self.nodes = int(self.nodes * 0.97)

        # Prevent collapse
        if self.nodes < 5:
            self.nodes = 5

        # ----------------------------
        # STABILITY SCORE
        # ----------------------------

        stability = 1 - abs(self.entropy - self.TARGET_ENTROPY)

        # If unstable → reduce activity
        if stability < 0.6:
            self.temp *= 0.9
            self.nodes = int(self.nodes * 0.98)

        # ----------------------------
        # MEMORY + SELF-AWARENESS
        # ----------------------------

        self.history.append({
            "tick": self.tick,
            "entropy": round(self.entropy, 3),
            "temp": round(self.temp, 3),
            "nodes": self.nodes,
            "stability": round(stability, 3)
        })

        # Keep memory bounded
        if len(self.history) > 500:
            self.history.pop(0)

        # ----------------------------
        # OUTPUT
        # ----------------------------

        print(f"[V53] tick={self.tick} | entropy={self.entropy:.3f} | temp={self.temp:.3f} | nodes={self.nodes} | stability={stability:.3f}")

    # ----------------------------
    # Utilities
    # ----------------------------

    def clamp(self, x, min_val, max_val):
        return max(min(x, max_val), min_val)

    # ----------------------------
    # Run Loop
    # ----------------------------

    def run(self):
        try:
            while True:
                self.step()
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[V53] shutdown clean")
            self.summary()

    def summary(self):
        avg_entropy = sum(x["entropy"] for x in self.history) / len(self.history)
        avg_stability = sum(x["stability"] for x in self.history) / len(self.history)

        print("\n[V53 SUMMARY]")
        print(f"Avg Entropy: {avg_entropy:.3f}")
        print(f"Avg Stability: {avg_stability:.3f}")
        print(f"Final Nodes: {self.nodes}")


# ----------------------------
# BOOT
# ----------------------------

if __name__ == "__main__":
    omega = OmegaV53()
    omega.run()
