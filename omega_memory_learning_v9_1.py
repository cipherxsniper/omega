# 🧠 OMEGA v9.1 PERSISTENT NODE MEMORY + LEARNING LOOP

import time
import json

class NodeMemoryStore:
    def __init__(self):
        self.memory = {}

    def record(self, node, score, decision, outcome=0.0):
        if node not in self.memory:
            self.memory[node] = []

        self.memory[node].append({
            "score": score,
            "decision": decision,
            "outcome": outcome,
            "timestamp": time.time()
        })

    def get_history(self, node):
        return self.memory.get(node, [])


class LearningEngineV9_1:
    def update_score(self, history):
        if not history:
            return 0.5

        total = 0
        weight = 0

        for h in history:
            impact = h.get("outcome", 0.0)
            score = h.get("score", 0.5)

            total += score * (1 + impact)
            weight += 1

        return max(0.0, min(1.0, total / weight))


class OmegaV9_1Loop:
    def __init__(self, memory_store, decision_engine):
        self.memory = memory_store
        self.decision_engine = decision_engine
        self.learning = LearningEngineV9_1()

    def step(self, node, metrics):
        history = self.memory.get_history(node)

        learned_score = self.learning.update_score(history)

        decision = self.decision_engine.decide(
            node,
            learned_score,
            metrics.get("error_rate", 0.0)
        )

        self.memory.record(
            node,
            learned_score,
            decision,
            outcome=metrics.get("outcome", 0.0)
        )

        return {
            "node": node,
            "learned_score": learned_score,
            "decision": decision
        }
