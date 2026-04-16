# ============================================================
# OMEGA DECISION ENGINE v5
# MULTI-BRAIN CONSENSUS + WEIGHTED INTELLIGENCE RESOLUTION
# ============================================================

import time
import traceback
from collections import defaultdict


# ============================================================
# ⚖️ DECISION ENGINE
# ============================================================

class OmegaDecisionEngine:
    def __init__(self, mesh, state, memory, graph, learning):
        self.mesh = mesh
        self.state = state
        self.memory = memory
        self.graph = graph
        self.learning = learning

        self.brain_outputs = defaultdict(list)
        self.weights = {
            "Brain00": 0.6,
            "Brain11": 0.7,
            "Brain22": 0.8,
            "ParallelBrain": 0.9
        }

        self._bind_events()

    # --------------------------------------------------------
    # EVENT BINDING
    # --------------------------------------------------------

    def _bind_events(self):
        self.mesh.subscribe("brain_thought", self.on_brain_thought)

    # --------------------------------------------------------
    # RECEIVE BRAIN OUTPUTS
    # --------------------------------------------------------

    def on_brain_thought(self, event):
        source = event.get("source")
        data = event.get("data", {})

        self.brain_outputs[source].append({
            "data": data,
            "timestamp": time.time()
        })

    # --------------------------------------------------------
    # WEIGHTED CONSENSUS CALCULATION
    # --------------------------------------------------------

    def calculate_consensus(self):
        scores = defaultdict(float)

        for brain, outputs in self.brain_outputs.items():
            weight = self.weights.get(brain, 0.5)

            for output in outputs:
                idea = output["data"].get("idea", "unknown")
                confidence = output["data"].get("confidence", 0.5)

                scores[idea] += weight * confidence

        if not scores:
            return {"decision": "idle", "confidence": 0.0}

        best_decision = max(scores, key=scores.get)

        return {
            "decision": best_decision,
            "confidence": scores[best_decision],
            "all_scores": dict(scores)
        }

    # --------------------------------------------------------
    # EXECUTE DECISION
    # --------------------------------------------------------

    def execute(self):
        try:
            result = self.calculate_consensus()

            decision_event = {
                "decision": result["decision"],
                "confidence": result["confidence"],
                "timestamp": time.time()
            }

            # STORE IN MEMORY
            self.memory.add_knowledge({
                "type": "decision",
                "data": decision_event
            })

            # UPDATE STATE
            self.state.update_metric("last_decision", decision_event)

            # LOG TO GRAPH
            self.graph.link("decision_engine", result["decision"], "selected_action")

            # BROADCAST RESULT
            self.mesh.publish(
                "system_decision",
                data=decision_event,
                source="decision_engine"
            )

            return decision_event

        except Exception as e:
            self.learning.record_failure("decision_engine", str(e))
            self.mesh.publish("system_error", str(e), source="decision_engine")
            traceback.print_exc()

