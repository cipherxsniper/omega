import time
import random
from collections import defaultdict

from omega_state import OmegaState
from omega_graph_memory_v36 import CognitiveGraphMemory


# =========================
# 🧠 SELF-MODIFYING COGNITIVE GRAPH
# =========================
class SelfModifyingGraph:
    def __init__(self):
        self.graph = CognitiveGraphMemory()

        # node energy = survival pressure
        self.energy = defaultdict(lambda: 1.0)

        # edge strength cache
        self.edge_strength = defaultdict(lambda: 0.5)

    # -------------------------
    # SCORE NODE
    # -------------------------
    def score(self, node_id):
        base = self.energy[node_id]
        return base

    # -------------------------
    # MUTATE NODE ENERGY
    # -------------------------
    def reinforce_node(self, node_id, reward):
        self.energy[node_id] += reward * 0.1

    def decay_nodes(self):
        for k in list(self.energy.keys()):
            self.energy[k] *= 0.995

            # prune dead nodes
            if self.energy[k] < 0.05:
                del self.energy[k]

    # -------------------------
    # EDGE LEARNING
    # -------------------------
    def reinforce_edge(self, a, b):
        key = (a, b)
        self.edge_strength[key] += 0.05

    def decay_edges(self):
        for k in list(self.edge_strength.keys()):
            self.edge_strength[k] *= 0.99

            if self.edge_strength[k] < 0.05:
                del self.edge_strength[k]

    # -------------------------
    # STRUCTURAL MUTATION
    # -------------------------
    def maybe_spawn_node(self, base_node):
        if random.random() < 0.1:
            new_node = base_node + "_gen"
            self.energy[new_node] = 0.5
            return new_node
        return None

    # -------------------------
    # UPDATE GRAPH
    # -------------------------
    def update(self, active_node):
        self.graph.update_node(active_node, self.energy[active_node])

        spawned = self.maybe_spawn_node(active_node)

        if spawned:
            self.graph.update_node(spawned, self.energy[spawned])

        self.reinforce_node(active_node, 1.0)

        self.decay_nodes()
        self.decay_edges()


# =========================
# 🧠 V39 KERNEL
# =========================
class OmegaKernelV39:
    def __init__(self):
        self.state = OmegaState()
        self.graph = SelfModifyingGraph()

        self.nodes = ["attention", "memory", "goal", "stability"]

        self.tick_rate = 1

    # -------------------------
    # GENERATE SIGNALS
    # -------------------------
    def generate(self):
        return {n: random.random() for n in self.nodes}

    # -------------------------
    # SELECT NEXT THOUGHT
    # -------------------------
    def select(self, signals):
        scored = []

        for n, v in signals.items():
            score = v * self.graph.score(n)
            scored.append((score, n))

        scored.sort(reverse=True)

        return scored[0][1]

    # -------------------------
    # STEP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        signals = self.generate()

        active = self.select(signals)

        self.graph.update(active)

        self.state.remember({
            "tick": tick,
            "active": active,
            "signals": signals
        })

        print(f"[V39] tick={tick} | active={active} | nodes={len(self.graph.energy)}")

    # -------------------------
    # RUN
    # -------------------------
    def run(self):
        print("[V39] SELF-MODIFYING COGNITIVE GRAPH ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV39().run()
