import random
import math
import time
import json
import os

class OmegaKernelV6_7:

    def __init__(self):
        self.tick_count = 0

        # 🧠 GLOBAL NODE INTELLIGENCE MEMORY
        self.node_memory = {}

        # 🌍 GLOBAL LEARNING STATE
        self.global_state = {
            "total_ticks": 0,
            "system_entropy": 0.7,
            "learning_rate": 0.05
        }

    # 🧠 INIT NODE MEMORY
    def _init_node(self, node):
        if node not in self.node_memory:
            self.node_memory[node] = {
                "success": 1.0,
                "failure": 1.0,
                "score": 0.5,
                "variance": 0.0,
                "history": [],
                "role": "unknown"
            }

    # 📊 UPDATE NODE INTELLIGENCE
    def update_node(self, node, success):
        mem = self.node_memory[node]

        if success:
            mem["success"] += 1
        else:
            mem["failure"] += 1

        total = mem["success"] + mem["failure"]

        # 🎯 INTELLIGENCE SCORE
        mem["score"] = mem["success"] / total

        # 🌪 VARIANCE (exploration vs instability)
        mem["variance"] = abs(mem["success"] - mem["failure"]) / total

        mem["history"].append(success)
        if len(mem["history"]) > 50:
            mem["history"].pop(0)

        # 🧠 ROLE CLASSIFICATION
        if mem["score"] > 0.75:
            mem["role"] = "stable_core"
        elif mem["score"] < 0.3:
            mem["role"] = "unstable"
        elif mem["variance"] > 0.6:
            mem["role"] = "explorer"
        else:
            mem["role"] = "balanced"

    # 🔮 ATTENTION (SOFTMAX DISTRIBUTION)
    def attention(self, nodes):
        scores = []

        for n in nodes:
            self._init_node(n)
            mem = self.node_memory[n]

            base = mem["score"]

            # entropy injection
            noise = random.uniform(-self.global_state["system_entropy"], self.global_state["system_entropy"])

            scores.append(base + noise)

        exp_scores = [math.exp(s) for s in scores]
        total = sum(exp_scores)

        attention_map = []
        for i, n in enumerate(nodes):
            att = exp_scores[i] / total
            attention_map.append({"node": n, "attention": att})

        return attention_map

    # 🎯 SELECT NODE
    def choose(self, attention_map):
        return max(attention_map, key=lambda x: x["attention"])["node"]

    # ⚙️ SIMULATED OUTCOME (replace later with real execution)
    def simulate(self, node):
        mem = self.node_memory[node]

        # nodes with higher score succeed more often
        prob = mem["score"]

        return random.random() < prob

    # 🧠 GLOBAL LEARNING ADAPTATION
    def update_global(self):
        avg_score = sum(n["score"] for n in self.node_memory.values()) / len(self.node_memory)

        # adapt entropy based on system performance
        if avg_score > 0.7:
            self.global_state["system_entropy"] *= 0.98
        else:
            self.global_state["system_entropy"] *= 1.02

        # clamp
        self.global_state["system_entropy"] = max(0.1, min(1.5, self.global_state["system_entropy"]))

    # 🧾 OBSERVABILITY
    def report(self, chosen, success, attention_map):
        return {
            "tick": self.tick_count,
            "chosen": chosen,
            "success": success,
            "entropy": self.global_state["system_entropy"],
            "top_nodes": sorted(
                [(n, m["score"], m["role"]) for n, m in self.node_memory.items()],
                key=lambda x: x[1],
                reverse=True
            )[:5],
            "attention": attention_map
        }

    # 🔁 MAIN TICK
    def tick(self, nodes):
        self.tick_count += 1
        self.global_state["total_ticks"] += 1

        # attention distribution
        attention_map = self.attention(nodes)

        # choose node
        chosen = self.choose(attention_map)

        # simulate result
        success = self.simulate(chosen)

        # update memory
        self.update_node(chosen, success)

        # global adaptation
        self.update_global()

        return self.report(chosen, success, attention_map)


# 🚀 AUTO-RUN MODE
if __name__ == "__main__":
    k = OmegaKernelV6_7()
    nodes = ["brain", "system", "executor", "observer"]

    while True:
        print(k.tick(nodes))
        time.sleep(0.5)
