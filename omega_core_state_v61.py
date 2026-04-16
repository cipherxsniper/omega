class OmegaCoreState:
    def __init__(self):
        self.scores = []
        self.drifts = []

    def record(self, score, drift):
        self.scores.append(score)
        self.drifts.append(drift)

    def avg_score(self):
        return sum(self.scores) / len(self.scores) if self.scores else 0.0

    def avg_drift(self):
        return sum(self.drifts) / len(self.drifts) if self.drifts else 0.0
