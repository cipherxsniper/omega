# core/reasoning_engine_v2.py

class ReasoningEngine:
    def __init__(self, shared_state):
        self.state = shared_state

    def reason(self, goal, prediction, context):
        decision = ""

        if goal == "optimize_decision":
            if prediction == "UP":
                decision = "reinforce strategy"
            else:
                decision = "modify strategy"

        elif goal == "expand_knowledge":
            decision = "integrate knowledge"

        elif goal == "analyze_environment":
            decision = "analyze patterns"

        elif goal == "improve_predictions":
            decision = "adjust prediction model"

        return decision
