# 🧠 v10.5 Ecosystem Router (Cross-node intelligence flow)

from omega_decision_engine_v10_5 import DecisionEngineV10_5

class ControlRouterV10_5:

    def __init__(self):
        self.engine = DecisionEngineV10_5()

    def run_cycle(self, nodes):

        results = {}

        for node in nodes:

            score, decision = self.engine.decide(node)

            self.engine.feedback(node, score, decision)

            results[node] = {
                "score": round(score, 3),
                "decision": decision
            }

        return results
