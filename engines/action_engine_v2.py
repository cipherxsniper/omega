# engines/action_engine_v2.py

class ActionEngine:
    def __init__(self, shared_state):
        self.state = shared_state

    def execute(self, decision):
        action = f"Executed: {decision}"
        self.state["actions"].append(action)
        return action
