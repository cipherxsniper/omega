import time
import random
import math
from collections import defaultdict, deque

from omega_state import OmegaState


# =========================
# 🧠 HIERARCHY ENGINE
# =========================
class HierarchyEngine:
    def __init__(self):
        self.node_score = defaultdict(float)
        self.node_level = defaultdict(int)
        self.cluster_map = defaultdict(list)
        self.history = deque(maxlen=300)

    # -------------------------
    # SCORE UPDATE
    # -------------------------
    def update(self, signals):
        for node, value in signals.items():
            self.node_score[node] += value * 0.1

            # decay prevents infinite inflation
            self.node_score[node] *= 0.997

        self._compute_hierarchy()

    # -------------------------
    # HIERARCHY ASSIGNMENT
    # -------------------------
    def _compute_hierarchy(self):
        if not self.node_score:
            return

        sorted_nodes = sorted(
            self.node_score.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top_20 = sorted_nodes[:len(sorted_nodes)//2 or 1]
        mid_30 = sorted_nodes[len(sorted_nodes)//2:][:3]
        rest = sorted_nodes[3:]

        # Level system
        for n, _ in top_20:
            self.node_level[n] = 3  # executive

        for n, _ in mid_30:
            self.node_level[n] = 2  # active

        for n, _ in rest:
            self.node_level[n] = 1  # background

        # cluster formation
        self.cluster_map["executive"] = [n for n, _ in top_20]
        self.cluster_map["active"] = [n for n, _ in mid_30]
        self.cluster_map["background"] = [n for n, _ in rest]

    # -------------------------
    # GET ACTIVE EXECUTIVE NODE
    # -------------------------
    def get_leader(self):
        if not self.node_score:
            return "null"

        return max(self.node_score.items(), key=lambda x: x[1])[0]


# =========================
# 🧠 V44 KERNEL
# =========================
class OmegaKernelV44:
    def __init__(self):
        self.state = OmegaState()
        self.hierarchy = HierarchyEngine()

        self.nodes = ["attention", "memory", "goal", "stability"]

        self.tick_rate = 1

    # -------------------------
    # SIGNAL GENERATION
    # -------------------------
    def generate_signals(self):
        return {
            n: random.uniform(0.2, 1.5) * random.random()
            for n in self.nodes
        }

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        signals = self.generate_signals()

        # update hierarchy engine
        self.hierarchy.update(signals)

        leader = self.hierarchy.get_leader()

        executive = self.hierarchy.cluster_map["executive"]
        active = self.hierarchy.cluster_map["active"]

        self.state.remember({
            "tick": tick,
            "leader": leader,
            "executive_nodes": executive,
            "active_nodes": active
        })

        print(
            f"[V44] tick={tick} | "
            f"leader={leader} | "
            f"exec={len(executive)} | "
            f"active={len(active)}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V44] EMERGENT HIERARCHY COGNITION ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV44().run()
