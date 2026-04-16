import time
from collections import deque

# ================================
# Ω TEMPORAL DRIFT MEMORY v4.6
# ================================

class TemporalDriftMemory:
    def __init__(self, maxlen=50):
        # stores (timestamp, score, drift_count)
        self.history = deque(maxlen=maxlen)

    def record(self, score, drift_count):
        self.history.append((time.time(), score, drift_count))

    def get_velocity(self):
        """
        Measures rate of change in system health
        """
        if len(self.history) < 2:
            return 0.0

        (t1, s1, d1), (t2, s2, d2) = self.history[0], self.history[-1]

        time_delta = max(t2 - t1, 1)
        score_delta = s2 - s1

        return score_delta / time_delta

    def get_trend(self):
        """
        Classifies system behavior over time
        """
        if len(self.history) < 5:
            return "insufficient_data"

        scores = [s for _, s, _ in self.history]

        if scores[-1] > scores[0] + 0.05:
            return "improving"

        if abs(scores[-1] - scores[0]) <= 0.05:
            return "stable"

        if scores[-1] < scores[0] - 0.10:
            return "degrading"

        return "unstable"


def temporal_gate(memory: TemporalDriftMemory, current_score, drift_count):
    """
    HARD EXECUTION GATE (v4.6)
    """

    memory.record(current_score, drift_count)

    velocity = memory.get_velocity()
    trend = memory.get_trend()

    print(f"""
[Ω TEMPORAL GATE]

Score: {current_score:.2f}
Drift: {drift_count}
Velocity: {velocity:.4f}
Trend: {trend}
""")

    # ================================
    # BLOCK CONDITIONS
    # ================================

    if trend == "degrading":
        print("[Ω TEMPORAL] BLOCKED: system degrading over time")
        return False

    if drift_count > 30:
        print("[Ω TEMPORAL] BLOCKED: excessive drift pressure")
        return False

    if velocity < -0.02:
        print("[Ω TEMPORAL] BLOCKED: rapid coherence decay detected")
        return False

    print("[Ω TEMPORAL] APPROVED: system temporally stable\n")
    return True
