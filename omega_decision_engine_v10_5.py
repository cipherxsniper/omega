# 🧠 v10.5 Memory-Aware Decision Engine

from omega_scoring_core_v9 import AdaptiveScoringCore
from omega_memory_graph_v10_5 import MemoryGraph

class DecisionEngineV10_5:

    def __init__(self):
        self.scorer = AdaptiveScoringCore()
        self.memory = MemoryGraph()

    def decide(self, node, input_signal=0.0):

        mem = self.memory.read(node)

        # 🧠 memory influences score
        memory_bias = mem["activation"] * 0.1

        score = self.scorer.compute_score(node, input_signal + memory_bias)

        if score > 0.78:
            decision = "ACTIVATE"
        elif score > 0.55:
            decision = "MONITOR"
        else:
            decision = "NO_ACTION"

        return score, decision

    def feedback(self, node, score, decision):

        result = (
            "SUCCESS" if decision == "ACTIVATE"
            else "STABLE" if decision == "MONITOR"
            else "FAIL"
        )

        self.scorer.update(node, score, result)

        # 🧠 WRITE TO SHARED MEMORY GRAPH
        self.memory.write(node, "cycle_update", score, decision)
