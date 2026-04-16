# ================================
# Ω MEMORY ADAPTER v6
# Bridges kernel ↔ temporal system
# ================================

class OmegaMemoryAdapter:
    def __init__(self):
        self.score_history = []
        self.drift_history = []

    def record(self, score, drift):
        self.score_history.append(score)
        self.drift_history.append(drift)

    def recent(self, n=20):
        return {
            "scores": self.score_history[-n:],
            "drift": self.drift_history[-n:]
        }

    def avg_score(self):
        return sum(self.score_history) / len(self.score_history) if self.score_history else 0.0

    def avg_drift(self):
        return sum(self.drift_history) / len(self.drift_history) if self.drift_history else 0.0
