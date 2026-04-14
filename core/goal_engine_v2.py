# core/goal_engine_v2.py

import random

class GoalEngine:
    def __init__(self, shared_state):
        self.state = shared_state

    def generate_goal(self):
        possible = [
            "analyze_environment",
            "expand_knowledge",
            "optimize_decision",
            "improve_predictions"
        ]

        goal = {
            "goal": random.choice(possible),
            "priority": random.randint(1, 3)
        }

        self.state["goals"].append(goal)
        return goal

    def get_active_goal(self):
        if not self.state["goals"]:
            return self.generate_goal()
        return self.state["goals"][-1]

    def complete_goal(self):
        if self.state["goals"]:
            self.state["goals"].pop(0)
