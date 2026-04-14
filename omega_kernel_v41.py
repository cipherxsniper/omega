import time
import random
import math
from collections import defaultdict, deque, Counter

from omega_state import OmegaState


# =========================
# 🧠 META-EVALUATION ENGINE
# =========================
class MetaEvaluator:
    def __init__(self):
        # learned scoring weights (THIS is the self-modifying core)
        self.weights = defaultdict(lambda: 1.0)

        self.reward_trace = deque(maxlen=200)
        self.entropy_target = 1.2  # adaptive cognition goal

    # -------------------------
    # DYNAMIC SCORING FUNCTION
    # -------------------------
    def score(self, node, signal, entropy_gap):
        base = self.weights[node]

        # policy shaping
        stability_bonus = 1.0 / (1.0 + abs(entropy_gap))
        signal_factor = signal

        return base * signal_factor * stability_bonus

    # -------------------------
    # SELF-MODIFYING UPDATE
    # -------------------------
    def learn(self, selected_node, reward, entropy_gap):
        self.reward_trace.append(reward)

        # reinforce selected node
        self.weights[selected_node] += reward * 0.05

        # entropy-driven reshaping (core innovation)
        if entropy_gap > 0:
            # too chaotic → strengthen stability nodes
            self.weights["stability"] *= 1.02
        else:
            # too ordered → strengthen exploration nodes
            self.weights["attention"] *= 1.02

        # global decay (prevents runaway divergence)
        for k in list(self.weights.keys()):
            self.weights[k] *= 0.998

    # -------------------------
    # ADAPTIVE ENTROPY TARGETING
    # -------------------------
    def adjust_target(self, entropy):
        error = self.entropy_target - entropy

        # slow-moving target adaptation
        self.entropy_target += error * 0.01


# =========================
# 🧠 V41 COGNITIVE KERNEL
# =========================
class OmegaKernelV41:
    def __init__(self):
        self.state = OmegaState()
        self.meta = MetaEvaluator()

        self.nodes = ["attention", "memory", "goal", "stability"]

        self.history = deque(maxlen=100)

        self.tick_rate = 1

    # -------------------------
    # SIGNAL GENERATION
    # -------------------------
    def generate_signals(self):
        return {n: random.random() for n in self.nodes}

    # -------------------------
    # ENTROPY CALCULATION
    # -------------------------
    def compute_entropy(self):
        counts = Counter(self.history)
        total = len(self.history) + 1e-9

        entropy = 0.0
        for c in counts.values():
            p = c / total
            entropy -= p * math.log(p + 1e-9)

        return entropy

    # -------------------------
    # NODE SELECTION (META POLICY)
    # -------------------------
    def select(self, signals, entropy_gap):
        scored = []

        for node, signal in signals.items():
            score = self.meta.score(node, signal, entropy_gap)
            scored.append((score, node))

        scored.sort(reverse=True)
        return scored[0][1]

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        signals = self.generate_signals()

        entropy = self.compute_entropy()
        entropy_gap = self.meta.entropy_target - entropy

        selected = self.select(signals, entropy_gap)

        # history for entropy evolution
        self.history.append(selected)

        # fake reward signal (replace later with real environment feedback)
        reward = signals[selected] * (1.0 + abs(entropy_gap))

        # learning update
        self.meta.learn(selected, reward, entropy_gap)
        self.meta.adjust_target(entropy)

        # memory write
        self.state.remember({
            "tick": tick,
            "selected": selected,
            "entropy": entropy,
            "entropy_target": self.meta.entropy_target,
            "weights": dict(self.meta.weights)
        })

        print(
            f"[V41] tick={tick} | "
            f"selected={selected} | "
            f"entropy={entropy:.3f} | "
            f"target={self.meta.entropy_target:.3f} | "
            f"nodes={len(self.meta.weights)}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V41] META-EVALUATION COGNITION ENGINE ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV41().run()
