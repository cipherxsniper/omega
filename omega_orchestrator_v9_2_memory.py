from omega_event_memory_v9_3 import *
from omega_scoring_core_v9 import ScoringCoreV9
from omega_decision_engine_v9 import DecisionEngineV9
from omega_policy_simulator_v9 import PolicySimulatorV9
from omega_control_router_v9 import ControlRouterV9
import time


NODES = ["node_memory", "node_goal", "node_attention", "node_stability"]


class OmegaOrchestratorV9_3:

    def __init__(self):
        self.memory = EventMemoryV9_3()

        self.scorer = ScoringCoreV9()
        self.decision_engine = DecisionEngineV9()
        self.simulator = PolicySimulatorV9()
        self.router = ControlRouterV9()

    def metrics(self, node):
        return {
            "stability": 0.6,
            "output_quality": 0.7,
            "latency": 0.3,
            "error_rate": 0.2
        }

    def cycle(self, node):

        m = self.metrics(node)

        base_score = self.scorer.score_node(m)

        # 🧠 MEMORY BIAS APPLIED
        score = self.memory.bias_score(node, base_score)

        decision = self.decision_engine.decide(
            node,
            score,
            m["error_rate"]
        )

        sim = self.simulator.simulate(decision, node, score)

        self.memory.record(node, score, decision, sim.risk)

        result = self.router.apply({
            "node": node,
            "decision": decision,
            "risk": sim.risk,
            "score": score
        })

        return {
            "node": node,
            "score": score,
            "decision": decision,
            "trend": self.memory.trend(node),
            "status": result["status"]
        }

    def run(self):

        print("🧠 OMEGA v9.3 EVENT MEMORY ONLINE")

        while True:
            for node in NODES:
                out = self.cycle(node)

                print(f"[{out['node']}] "
                      f"score={out['score']:.3f} "
                      f"decision={out['decision']} "
                      f"trend={out['trend']} "
                      f"status={out['status']}")

            time.sleep(2)


if __name__ == "__main__":
    OmegaOrchestratorV9_3().run()
