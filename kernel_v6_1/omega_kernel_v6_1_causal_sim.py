import random
import math
from collections import defaultdict

class OmegaKernelV6_1:

    def __init__(self):
        # node state memory
        self.node_memory = defaultdict(lambda: {
            "success": 1.0,
            "failure": 1.0,
            "variance": 0.0
        })

        self.policy = {
            "exploration_bias": 0.5,
            "stability_bias": 0.5,
            "entropy": 0.3
        }

    # -----------------------------
    # 1. BRANCHING FUTURES
    # -----------------------------
    def simulate_futures(self, nodes, depth=3):
        futures = []

        for node in nodes:
            for i in range(depth):
                noise = random.uniform(-self.policy["entropy"], self.policy["entropy"])

                score = self.score_node(node) + noise

                futures.append({
                    "node": node,
                    "depth": i,
                    "predicted_score": score
                })

        return futures

    # -----------------------------
    # 2. SCORING FUNCTION
    # stability vs exploration
    # -----------------------------
    def score_node(self, node):
        mem = self.node_memory[node]

        stability = mem["success"] / (mem["success"] + mem["failure"] + 1e-6)
        exploration = self.policy["exploration_bias"]

        return (
            stability * self.policy["stability_bias"] +
            exploration * random.random()
        )

    # -----------------------------
    # 3. DISTRIBUTED ATTENTION
    # softmax activation
    # -----------------------------
    def attention_distribution(self, futures):
        scores = [f["predicted_score"] for f in futures]

        max_s = max(scores) if scores else 1.0

        exp_scores = [math.exp(s - max_s) for s in scores]
        total = sum(exp_scores) or 1.0

        return [
            {
                "node": f["node"],
                "attention": e / total,
                "score": f["predicted_score"]
            }
            for f, e in zip(futures, exp_scores)
        ]

    # -----------------------------
    # 4. MEMORY FEEDBACK LOOP
    # -----------------------------
    def update_memory(self, node, success=True):
        mem = self.node_memory[node]

        if success:
            mem["success"] += 1
        else:
            mem["failure"] += 1

        total = mem["success"] + mem["failure"]
        mem["variance"] = abs(mem["success"] - mem["failure"]) / total

    # -----------------------------
    # 5. MAIN TICK (Causal Engine)
    # -----------------------------
    def tick(self, nodes):
        futures = self.simulate_futures(nodes)

        attention = self.attention_distribution(futures)

        chosen = max(attention, key=lambda x: x["attention"])

        # simulate outcome
        success = random.random() < 0.7

        self.update_memory(chosen["node"], success)

        return {
            "futures": futures,
            "attention_map": attention,
            "chosen": chosen,
            "success": success,
            "memory_snapshot": dict(self.node_memory)
        }
