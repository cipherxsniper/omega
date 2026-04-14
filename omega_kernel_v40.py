import time
import random
import math
from collections import defaultdict, Counter, deque

from omega_state import OmegaState


# =========================
# 🧠 ENTROPY CONTROLLER
# =========================
class EntropyController:
    def __init__(self):
        self.history = deque(maxlen=100)
        self.temperature = 1.0

    # -------------------------
    # SHANNON ENTROPY (FIXED)
    # -------------------------
    def compute_entropy(self, active_nodes):
        counts = Counter(active_nodes)
        total = len(active_nodes) + 1e-9

        entropy = 0.0

        for c in counts.values():
            p = c / total
            entropy -= p * math.log(p + 1e-9)

        return entropy

    # -------------------------
    # TEMPERATURE CONTROL LOOP
    # -------------------------
    def update_temperature(self, entropy):
        self.history.append(entropy)

        avg = sum(self.history) / len(self.history)

        # stable entropy band
        if avg < 0.2:
            self.temperature *= 1.05  # too ordered → explore
        elif avg > 1.5:
            self.temperature *= 0.95  # too chaotic → stabilize

        self.temperature = max(0.4, min(2.5, self.temperature))


# =========================
# 🧠 COGNITIVE GRAPH CORE
# =========================
class CognitiveGraph:
    def __init__(self):
        self.energy = defaultdict(lambda: 1.0)
        self.activation_count = defaultdict(int)

    # -------------------------
    # SCORING FUNCTION
    # -------------------------
    def score(self, node, temperature):
        base = self.energy[node]
        rarity = 1.0 / (1.0 + self.activation_count[node])
        return base * rarity * temperature

    # -------------------------
    # UPDATE NODE STATE
    # -------------------------
    def update(self, node):
        self.energy[node] += 0.15
        self.activation_count[node] += 1

        # anti-dominance damping
        if self.energy[node] > 3.0:
            self.energy[node] *= 0.85

        # global decay (prevents runaway growth)
        for k in list(self.energy.keys()):
            self.energy[k] *= 0.995

        # prune dead nodes
        for k in list(self.energy.keys()):
            if self.energy[k] < 0.05:
                del self.energy[k]


# =========================
# 🧠 V40 KERNEL
# =========================
class OmegaKernelV40:
    def __init__(self):
        self.state = OmegaState()

        self.graph = CognitiveGraph()
        self.entropy = EntropyController()

        self.nodes = ["attention", "memory", "goal", "stability"]

        self.tick_rate = 1

    # -------------------------
    # SIGNAL GENERATION
    # -------------------------
    def generate_signals(self):
        return {n: random.random() for n in self.nodes}

    # -------------------------
    # NODE SELECTION
    # -------------------------
    def select_node(self, signals):
        scored = []

        for node, signal in signals.items():
            score = self.graph.score(node, self.entropy.temperature) * signal
            scored.append((score, node))

        scored.sort(reverse=True)
        return scored[0][1]

    # -------------------------
    # STEP FUNCTION
    # -------------------------
    def step(self):
        tick = self.state.tick()

        signals = self.generate_signals()
        active = self.select_node(signals)

        # update graph
        self.graph.update(active)

        # entropy computed from active distribution (expanded window)
        window = list(self.graph.activation_count.keys())
        entropy_val = self.entropy.compute_entropy(window)

        self.entropy.update_temperature(entropy_val)

        # memory write
        self.state.remember({
            "tick": tick,
            "active": active,
            "temperature": self.entropy.temperature,
            "entropy": entropy_val
        })

        print(
            f"[V40] tick={tick} | "
            f"active={active} | "
            f"temp={self.entropy.temperature:.3f} | "
            f"entropy={entropy_val:.3f} | "
            f"nodes={len(self.graph.energy)}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V40] STABILIZED ENTROPY COGNITION SYSTEM ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV40().run()
