import random

class GoalEngine:
    def __init__(self):
        self.goals = [
            {"goal": "learn_patterns", "priority": 1},
            {"goal": "improve_predictions", "priority": 2},
        ]
        self.completed = []

    def get_active_goal(self):
        if not self.goals:
            self.generate_new_goal()
        return sorted(self.goals, key=lambda x: x["priority"])[0]

    def complete_goal(self, goal):
        self.completed.append(goal)
        self.goals = [g for g in self.goals if g != goal]

    def generate_new_goal(self):
        new_goals = [
            "analyze_environment",
            "optimize_decision",
            "expand_knowledge"
        ]
        g = {
            "goal": random.choice(new_goals),
            "priority": random.randint(1, 3)
        }
        self.goals.append(g)
        return g
