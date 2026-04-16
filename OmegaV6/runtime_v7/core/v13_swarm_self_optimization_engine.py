import time
from collections import defaultdict


class SwarmSelfOptimizationEngineV13:
    """
    V13 Self-Optimization Layer

    Turns swarm cognition into a learning system:
    - evaluates decisions
    - scores outcomes
    - reinforces successful actions
    - weakens poor strategies
    """

    def __init__(self, memory, cognition_layer):
        self.memory = memory
        self.cognition = cognition_layer

        # strategy scoring table
        self.strategy_scores = defaultdict(lambda: {
            "success": 0,
            "failure": 0,
            "total": 0,
            "weight": 1.0
        })

        print("[V13 OPTIMIZER] ONLINE")

    # -----------------------------
    # MAIN OPTIMIZATION LOOP
    # -----------------------------
    def cycle(self):
        """
        1. run cognition
        2. evaluate last action
        3. update strategy weights
        """

        decision = self.cognition.cycle()

        outcome = self._simulate_outcome(decision)

        self._learn(decision, outcome)

        self._apply_adjustments()

        return {
            "decision": decision,
            "outcome": outcome
        }

    # -----------------------------
    # OUTCOME SIMULATION
    # (replace later with real metrics)
    # -----------------------------
    def _simulate_outcome(self, decision):
        action = decision.get("action")

        # simple heuristic scoring model
        if action == "stabilize":
            return {"result": "success", "score": 0.9}

        if action == "optimize_routes":
            return {"result": "success", "score": 0.7}

        if action == "probe_network":
            return {"result": "mixed", "score": 0.5}

        return {"result": "neutral", "score": 0.4}

    # -----------------------------
    # LEARNING CORE
    # -----------------------------
    def _learn(self, decision, outcome):
        action = decision.get("action")

        stats = self.strategy_scores[action]

        stats["total"] += 1

        if outcome["result"] == "success":
            stats["success"] += 1
        elif outcome["result"] == "failure":
            stats["failure"] += 1

        # reinforcement formula
        success_rate = stats["success"] / max(stats["total"], 1)

        stats["weight"] = 0.5 + success_rate

        print(f"[V13 LEARN] action={action} success_rate={success_rate:.2f}")

    # -----------------------------
    # STRATEGY ADJUSTMENT ENGINE
    # -----------------------------
    def _apply_adjustments(self):
        """
        Adjusts system behavior weights
        based on learned performance
        """

        best_strategy = max(
            self.strategy_scores.items(),
            key=lambda x: x[1]["weight"]
        )

        action, stats = best_strategy

        print(f"[V13 OPTIMIZED STRATEGY] {action} | weight={stats['weight']:.2f}")

        # inject optimization event into memory graph
        self.memory.add_event({
            "node_id": "v13_optimizer",
            "type": "optimization_update",
            "timestamp": time.time(),
            "best_action": action,
            "weight": stats["weight"]
        })


# -----------------------------
# FACTORY
# -----------------------------
def create_optimizer(memory, cognition):
    return SwarmSelfOptimizationEngineV13(memory, cognition)

def start():
    print("[V13] STARTED PERSISTENT LOOP")
    while True:
        time.sleep(1)

if __name__ == "__main__":
    import time
    start()

