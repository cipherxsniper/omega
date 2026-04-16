import math
from collections import deque

# ================================
# Ω SELF REGULATION LOOP v5.1
# ================================

class OmegaSelfRegulation:
    def __init__(self):
        self.drift_history = deque(maxlen=50)
        self.score_history = deque(maxlen=50)
        self.threshold = 0.75

    # ----------------------------
    # STATE UPDATE
    # ----------------------------
    def update(self, score, drift):
        self.score_history.append(score)
        self.drift_history.append(drift)

    # ----------------------------
    # VELOCITY (trend direction)
    # ----------------------------
    def compute_velocity(self):
        if len(self.score_history) < 2:
            return 0.0
        return self.score_history[-1] - self.score_history[-2]

    # ----------------------------
    # ADAPTIVE THRESHOLD ENGINE
    # ----------------------------
    def adaptive_threshold(self):
        if len(self.drift_history) < 5:
            return self.threshold

        avg_drift = sum(self.drift_history) / len(self.drift_history)
        velocity = self.compute_velocity()

        # instability → stricter system
        if velocity < -0.05:
            self.threshold *= 0.98

        # recovery → slightly more sensitive
        elif velocity > 0:
            self.threshold *= 1.01

        # clamp safety bounds
        self.threshold = max(0.4, min(0.9, self.threshold))

        return self.threshold

    # ----------------------------
    # DRIFT DAMPING LAYER
    # ----------------------------
    def damp_drift(self):
        if not self.drift_history:
            return

        avg = sum(self.drift_history) / len(self.drift_history)

        if avg > 25:
            self.drift_history = deque(
                [d * 0.92 for d in self.drift_history],
                maxlen=50
            )

    # ----------------------------
    # SOFT RECOVERY PULSE
    # ----------------------------
    def recovery_pulse(self, score):
        if not self.score_history:
            return score

        avg = sum(self.score_history) / len(self.score_history)

        # if degrading → slight stabilization bias
        if avg < 0.6:
            return min(1.0, score + 0.03)

        return score

    # ----------------------------
    # MAIN REGULATION CYCLE
    # ----------------------------
    def regulate(self, score, drift):
        self.update(score, drift)

        # apply damping first
        self.damp_drift()

        # recovery correction
        score = self.recovery_pulse(score)

        # recompute threshold
        threshold = self.adaptive_threshold()

        velocity = self.compute_velocity()
        avg_drift = sum(self.drift_history) / len(self.drift_history)

        # ----------------------------
        # SYSTEM STATE OUTPUT
        # ----------------------------
        state = "stable"

        if velocity < -0.05:
            state = "degrading"
        if avg_drift > 35:
            state = "unstable"

        return {
            "score": score,
            "drift": drift,
            "threshold": threshold,
            "velocity": velocity,
            "state": state,
            "avg_drift": avg_drift
        }
