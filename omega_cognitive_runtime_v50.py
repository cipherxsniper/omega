import time
from collections import deque

# ================================
# Ω COGNITIVE RUNTIME v5.0
# SINGLE UNIFIED CONTROL BRAIN
# ================================

class OmegaRuntime:

    def __init__(self):
        self.score_history = deque(maxlen=50)
        self.drift_history = deque(maxlen=50)

    # ================================
    # CORE INGESTION LOOP
    # ================================
    def ingest(self, event_type, module, score, drift):

        timestamp = time.time()

        # store state
        self.score_history.append(score)
        self.drift_history.append(drift)

        # compute intelligence signals
        avg_score = sum(self.score_history) / len(self.score_history)
        avg_drift = sum(self.drift_history) / len(self.drift_history)

        velocity = self._velocity()
        trend = self._trend(velocity)

        needs = self._detect_needs(avg_score, avg_drift, trend)

        actions = self._generate_actions(needs)

        # ================================
        # READABLE COGNITIVE FEED
        # ================================
        feed = f"""
[Ω COGNITIVE RUNTIME v5.0]

Time: {timestamp}

EVENT:
- Type: {event_type}
- Target: {module}

OBSERVATION:
- Score: {score:.2f}
- Drift: {drift}

SYSTEM STATE:
- Avg Score: {avg_score:.2f}
- Avg Drift: {avg_drift:.2f}
- Velocity: {velocity:.4f}
- Trend: {trend}

INFERENCE:
- {'System stability is degrading' if trend == 'degrading' else 'System stable or recovering'}

NEEDS DETECTED:
- {'\n- '.join(needs)}

RECOMMENDED ACTIONS:
- {'\n- '.join(actions)}
"""

        return {
            "feed": feed,
            "needs": needs,
            "actions": actions,
            "trend": trend,
            "avg_score": avg_score,
            "avg_drift": avg_drift
        }

    # ================================
    # TREND ENGINE
    # ================================
    def _velocity(self):
        if len(self.score_history) < 2:
            return 0.0
        return self.score_history[-1] - self.score_history[0]

    def _trend(self, velocity):
        if velocity > 0.05:
            return "improving"
        if velocity < -0.05:
            return "degrading"
        return "stable"

    # ================================
    # NEEDS ENGINE (SELF DIAGNOSIS)
    # ================================
    def _detect_needs(self, avg_score, avg_drift, trend):

        needs = []

        if avg_drift > 30:
            needs.append("drift_dampening_required")

        if avg_score < 0.65:
            needs.append("stability_recovery_required")

        if avg_drift > 40:
            needs.append("dependency_repair_required")

        if trend == "degrading":
            needs.append("predictive_stabilization_required")

        if not needs:
            needs.append("system_stable")

        return needs

    # ================================
    # ACTION ENGINE (NO AUTO EXECUTION)
    # ================================
    def _generate_actions(self, needs):

        actions = []

        if "drift_dampening_required" in needs:
            actions.append("apply drift smoothing layer")

        if "stability_recovery_required" in needs:
            actions.append("increase recovery pulse strength")

        if "dependency_repair_required" in needs:
            actions.append("run dependency graph scan")

        if "predictive_stabilization_required" in needs:
            actions.append("adjust future threshold prediction model")

        if "system_stable" in needs:
            actions.append("maintain current state")

        return actions
