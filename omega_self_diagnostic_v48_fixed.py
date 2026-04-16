from collections import deque

class OmegaSelfDiagnostic:
    def __init__(self):
        self.recent_scores = deque(maxlen=50)
        self.recent_drift = deque(maxlen=50)

    # ================================
    # COMPATIBILITY LAYER (FIX)
    # ================================
    def record(self, score, drift):
        self.recent_scores.append(score)
        self.recent_drift.append(drift)

    def update(self, score, drift):
        self.record(score, drift)

    def get_history(self):
        return list(self.recent_scores), list(self.recent_drift)

    # ================================
    # ANALYSIS CORE
    # ================================
    def detect_needs(self):
        if not self.recent_scores:
            return ["initializing"]

        avg_score = sum(self.recent_scores) / len(self.recent_scores)
        avg_drift = sum(self.recent_drift) / len(self.recent_drift)

        needs = []

        if avg_drift > 30:
            needs.append("drift_dampening_required")

        if avg_score < 0.6:
            needs.append("stability_recovery_required")

        if avg_score < 0.5 and avg_drift > 25:
            needs.append("threshold_relaxation_required")

        if avg_drift > 40:
            needs.append("dependency_repair_required")

        if not needs:
            needs.append("system_stable")

        return needs

    def report(self):
        needs = self.detect_needs()

        avg_score = sum(self.recent_scores)/len(self.recent_scores) if self.recent_scores else 0
        avg_drift = sum(self.recent_drift)/len(self.recent_drift) if self.recent_drift else 0

        return f"""
[Ω SELF DIAGNOSTIC FEED]

Average Score: {avg_score:.2f}
Average Drift: {avg_drift:.2f}

System Needs:
- {'\n- '.join(needs)}
"""
