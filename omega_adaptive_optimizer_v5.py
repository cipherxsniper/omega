# ============================================================
# OMEGA ADAPTIVE OPTIMIZER v5
# SELF-IMPROVING INTELLIGENCE WEIGHT EVOLUTION ENGINE
# ============================================================

import time
import traceback


# ============================================================
# 🧬 ADAPTIVE OPTIMIZER
# ============================================================

class OmegaAdaptiveOptimizer:
    def __init__(self, mesh, state, decision_engine, learning_engine):
        self.mesh = mesh
        self.state = state
        self.decision_engine = decision_engine
        self.learning_engine = learning_engine

        self.history = []
        self.adjustment_rate = 0.05  # controlled evolution speed

        self._bind_events()

    # --------------------------------------------------------
    # EVENT SYSTEM
    # --------------------------------------------------------

    def _bind_events(self):
        self.mesh.subscribe("system_decision", self.on_decision)
        self.mesh.subscribe("system_outcome", self.on_outcome)

    # --------------------------------------------------------
    # DECISION TRACKING
    # --------------------------------------------------------

    def on_decision(self, event):
        decision = event.get("data", {})

        self.history.append({
            "type": "decision",
            "data": decision,
            "timestamp": time.time()
        })

    # --------------------------------------------------------
    # OUTCOME FEEDBACK LOOP
    # --------------------------------------------------------

    def on_outcome(self, event):
        outcome = event.get("data", {})
        success = outcome.get("success", False)

        self.update_brain_weights(success)

    # --------------------------------------------------------
    # CORE EVOLUTION LOGIC
    # --------------------------------------------------------

    def update_brain_weights(self, success):
        weights = self.decision_engine.weights

        for brain in weights:
            if success:
                weights[brain] = min(weights[brain] + self.adjustment_rate, 1.0)
            else:
                weights[brain] = max(weights[brain] - self.adjustment_rate, 0.1)

        # persist evolution state
        self.state.update_metric("brain_weights", weights)
        self.state.update_metric("last_outcome_success", success)

        # store evolution event
        self.state.add_knowledge({
            "type": "adaptation",
            "weights": weights,
            "success": success
        })

        # broadcast evolution update
        self.mesh.publish(
            "system_adaptation",
            data={
                "weights": weights,
                "success": success
            },
            source="adaptive_optimizer"
        )

    # --------------------------------------------------------
    # ANALYSIS ENGINE
    # --------------------------------------------------------

    def analyze_system_evolution(self):
        total = len(self.history)
        if total == 0:
            return {"status": "no_data"}

        success_events = sum(
            1 for h in self.history
            if h.get("data", {}).get("confidence", 0) > 0.7
        )

        return {
            "total_events": total,
            "high_confidence_ratio": success_events / total
        }
