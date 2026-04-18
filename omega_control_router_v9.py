from omega_decision_engine_v9 import DecisionEngine
from omega_policy_simulator_v9 import PolicySimulator

class ControlRouter:
    def __init__(self):
        self.engine = DecisionEngine()
        self.sim = PolicySimulator()

    def route(self, nodes):
        results = {}

        for node in nodes:
            score, decision = self.engine.decide(node)

            prediction = self.sim.simulate(node, score)

            self.engine.feedback(node, score, decision)

            results[node] = {
                "score": score,
                "decision": decision,
                "prediction": prediction
            }

        return results
