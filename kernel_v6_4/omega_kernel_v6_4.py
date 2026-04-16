import random
import math
import time
from collections import defaultdict

class OmegaKernelV6_4:

    def __init__(self):
        self.nodes = defaultdict(lambda: {
            "success": 1.0,
            "failure": 1.0,
            "weight": 1.0
        })

        self.active_processes = 0
        self.max_processes = 6

        self.global_entropy = 0.6
        self.learning_rate = 0.05

        self.history = []

    # -------------------------
    # ⚡ EXECUTION GOVERNOR
    # -------------------------
    def can_execute(self):
        return self.active_processes < self.max_processes

    def register_process(self):
        self.active_processes += 1

    def release_process(self):
        self.active_processes = max(0, self.active_processes - 1)

    # -------------------------
    # 🧠 LEARNING SYSTEM
    # -------------------------
    def update_node(self, node, success):
        n = self.nodes[node]

        if success:
            n["success"] += 1
        else:
            n["failure"] += 1

        total = n["success"] + n["failure"]
        n["weight"] = n["success"] / total

    # -------------------------
    # 🌐 ATTENTION DISTRIBUTION
    # -------------------------
    def attention(self, candidates):
        scores = []

        for node in candidates:
            n = self.nodes[node]

            stability = n["weight"]
            exploration = random.uniform(0, self.global_entropy)

            score = (stability * 0.7) + (exploration * 0.3)

            scores.append((node, score))

        # soft distribution (not single collapse)
        total = sum(s for _, s in scores)
        distribution = [
            {"node": n, "attention": s / total}
            for n, s in scores
        ]

        return distribution

    # -------------------------
    # 🔮 EXECUTION STEP
    # -------------------------
    def tick(self, candidates):

        if not self.can_execute():
            return {
                "status": "blocked",
                "reason": "execution limit reached"
            }

        self.register_process()

        attention_map = self.attention(candidates)

        chosen = max(attention_map, key=lambda x: x["attention"])

        # simulate outcome
        success = random.random() < self.nodes[chosen["node"]]["weight"]

        self.update_node(chosen["node"], success)

        self.release_process()

        self.history.append({
            "chosen": chosen,
            "success": success
        })

        return {
            "active_processes": self.active_processes,
            "attention_map": attention_map,
            "chosen": chosen,
            "success": success,
            "node_state": dict(self.nodes)
        }
