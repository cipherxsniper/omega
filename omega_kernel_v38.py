import time
import random
from collections import defaultdict

from omega_state import OmegaState
from omega_graph_memory_v36 import CognitiveGraphMemory


# =========================
# 🧠 COGNITIVE SCHEDULER GRAPH
# =========================
class CognitiveScheduler:
    def __init__(self):
        self.graph = CognitiveGraphMemory()
        self.energy = defaultdict(lambda: 1.0)
def __init__(self):
    self.state = OmegaState()

    # 🧠 GRAPH MEMORY LAYER (MISSING PIECE)
    self.graph = CognitiveGraphMemory()

    # 🧠 COGNITIVE SCHEDULER
    self.scheduler = CognitiveScheduler()

    self.tick_rate = 1
    # -------------------------
    # NODE SCORING FUNCTION
    # -------------------------
    def score_node(self, node):
        base = node.get("value", 0.5)
        energy = self.energy[node["id"]]
        age_penalty = 1.0 / (1.0 + node.get("age", 1) * 0.01)

        return base * energy * age_penalty

    # -------------------------
    # SELECT NEXT THOUGHT
    # -------------------------
    def select_next(self, nodes):
        scored = []

        for n in nodes:
            score = self.score_node(n)
            scored.append((score, n))

        scored.sort(reverse=True, key=lambda x: x[0])

        return scored[0][1]  # winner takes cognition

    # -------------------------
    # ENERGY UPDATE (LEARNING)
    # -------------------------
    def update_energy(self, winner):
        self.energy[winner["id"]] += 0.05

        # decay others
        for k in self.energy:
            if k != winner["id"]:
                self.energy[k] *= 0.995


# =========================
# 🧠 V38 KERNEL
# =========================
class OmegaKernelV38:
    def __init__(self):
        self.state = OmegaState()
        self.scheduler = CognitiveScheduler()

        self.tick_rate = 1

    # -------------------------
    # COGNITIVE NODE GENERATION
    # -------------------------
    def generate_nodes(self):
        return [
            {"id": "attention", "value": random.uniform(0.3, 1.0)},
            {"id": "memory", "value": random.uniform(0.3, 1.0)},
            {"id": "goal", "value": random.uniform(0.3, 1.0)},
            {"id": "stability", "value": random.uniform(0.3, 1.0)},
        ]

    # -------------------------
    # EXECUTE SELECTED THOUGHT
    # -------------------------
    def execute(self, node):
        if node["id"] == "attention":
            return {"type": "focus_shift", "impact": 0.8}

        if node["id"] == "memory":
            return {"type": "recall", "impact": 0.6}

        if node["id"] == "goal":
            return {"type": "goal_update", "impact": 0.9}

        if node["id"] == "stability":
            return {"type": "stabilize", "impact": 0.7}

        return {"type": "noop", "impact": 0.1}

    # -------------------------
    # GRAPH UPDATE
    # -------------------------
    def update_graph(self, winner):
        self.graph.update_node(winner["id"], winner["value"])

        self.graph.reinforce_batch([winner["id"]])

    # -------------------------
    # CORE LOOP
    # -------------------------
    def step(self):
        tick = self.state.tick()

        nodes = self.generate_nodes()

        winner = self.scheduler.select_next(nodes)

        result = self.execute(winner)

        self.scheduler.update_energy(winner)

        self.update_graph(winner)

        self.state.remember({
            "tick": tick,
            "winner": winner,
            "result": result
        })

        print(
            f"[V38] tick={tick} | "
            f"next_thought={winner['id']} | "
            f"impact={result['impact']:.2f}"
        )

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):
        print("[V38] COGNITIVE SCHEDULER GRAPH ONLINE")

        while True:
            self.step()
            time.sleep(self.tick_rate)


if __name__ == "__main__":
    OmegaKernelV38().run()
