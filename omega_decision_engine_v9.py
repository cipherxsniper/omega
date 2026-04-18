from omega_scoring_core_v9 import AdaptiveScoringCore

class DecisionEngine:
    def __init__(self):
        self.scorer = AdaptiveScoringCore()

    def decide(self, node_name, input_signal=0.0):
        score = self.scorer.compute_score(node_name, input_signal)

        if score > 0.75:
            decision = "ACTIVATE"
        elif score > 0.55:
            decision = "MONITOR"
        else:
            decision = "NO_ACTION"

        return score, decision

    def feedback(self, node_name, score, decision):
        if decision == "ACTIVATE":
            result = "SUCCESS"
        elif decision == "NO_ACTION":
            result = "STABLE"
        else:
            result = "FAIL"

        self.scorer.update(node_name, score, result)
