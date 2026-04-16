# core/context_engine_v2.py

class ContextEngine:
    def __init__(self, shared_state):
        self.state = shared_state

    def build_context(self):
        memory = self.state["memory"][-10:]
        goals = self.state["goals"][-3:]
        predictions = self.state["predictions"][-3:]

        return {
            "recent_memory": memory,
            "active_goals": goals,
            "prediction_trend": predictions
        }
