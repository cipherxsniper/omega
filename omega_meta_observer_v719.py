class OmegaMetaObserverV719:

    def __init__(self):
        self.stability_history = []

    def score_stability(self, event, attention_score, risk_level):

        base = 1.0

        if event.get("event_type") == "success":
            base += 0.2
        elif event.get("event_type") == "route_error":
            base -= 0.4
        elif event.get("event_type") == "contract_violation":
            base -= 0.7

        if risk_level == "high_risk":
            base -= 0.3
        elif risk_level == "stable":
            base += 0.1

        stability = max(0.0, min(1.0, base))
        self.stability_history.append(stability)

        return stability

    def explain_tick(self, tick, event, attention_score, risk_level, stability):

        reason = []

        if event.get("event_type") == "success":
            reason.append("system executed valid routing path")

        if event.get("event_type") == "route_error":
            reason.append("execution layer failed during traversal")

        if attention_score > 1.5:
            reason.append("high attention node influenced decision path")

        if risk_level == "high_risk":
            reason.append("predictor flagged unstable state")

        if stability < 0.5:
            reason.append("system operating below stable threshold")

        return {
            "tick": tick,
            "stability": stability,
            "reasoning": reason,
            "summary": " | ".join(reason) if reason else "normal operation"
        }
