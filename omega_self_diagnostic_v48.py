from collections import deque

# ================================
# Ω SELF DIAGNOSTIC LAYER v4.8
# ================================

class OmegaSelfDiagnostic:
    def __init__(self):
        self.recent_scores = deque(maxlen=20)
        self.recent_drift = deque(maxlen=20)

    def update(self, score, drift):
        self.recent_scores.append(score)
        self.recent_drift.append(drift)

    # ================================
    # SYSTEM INTENT DETECTION
    # ================================
    def detect_needs(self):
        if not self.recent_scores:
            return ["initializing"]

        avg_score = sum(self.recent_scores) / len(self.recent_scores)
        avg_drift = sum(self.recent_drift) / len(self.recent_drift)

        needs = []

        # DRIFT CONTROL NEED
        if avg_drift > 30:
            needs.append("drift_dampening_required")

        # STABILITY NEED
        if avg_score < 0.6:
            needs.append("stability_recovery_required")

        # OVER-CORRECTION DETECTED
        if avg_score < 0.5 and avg_drift > 25:
            needs.append("threshold_relaxation_required")

        # SYSTEM FATIGUE
        if avg_drift > 40:
            needs.append("dependency_repair_required")

        if not needs:
            needs.append("system_stable")

        return needs

    # ================================
    # HUMAN READABLE INTELLIGENCE FEED
    # ================================
    def report(self):
        needs = self.detect_needs()

        return f"""
[Ω SELF DIAGNOSTIC FEED]

Average Score: {sum(self.recent_scores)/len(self.recent_scores) if self.recent_scores else 0:.2f}
Average Drift: {sum(self.recent_drift)/len(self.recent_drift) if self.recent_drift else 0:.2f}

System Needs:
- {chr(10).join(needs)}

Recommended Actions:
- auto-stabilize
- adjust thresholds if required
- reduce drift accumulation pressure
"""
