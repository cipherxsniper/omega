import time
import random

class GoalCore:

    def __init__(self):
        self.goals = [
            {"goal": "understand patterns", "priority": 0.8},
            {"goal": "stabilize memory", "priority": 0.9},
            {"goal": "increase coherence", "priority": 0.7}
        ]

    def generate_goal(self, signal):
        new_goal = {
            "goal": f"adapt to {signal}",
            "priority": random.uniform(0.4, 0.9)
        }
        self.goals.append(new_goal)

    def select_goal(self):
        return max(self.goals, key=lambda g: g["priority"])

    def decay(self):
        for g in self.goals:
            g["priority"] *= 0.99
