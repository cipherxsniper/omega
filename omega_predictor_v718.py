class OmegaPredictorV718:

    def predict_failure(self, event, graph_state):
        score = 0.0

        if event.get("event_type") == "route_error":
            score += 0.6

        if len(graph_state.get("nodes", {})) < 2:
            score += 0.3

        if event.get("node") is None:
            score += 0.5

        return min(score, 1.0)

    def classify(self, risk_score):
        if risk_score > 0.7:
            return "high_risk"
        if risk_score > 0.4:
            return "medium_risk"
        return "stable"
