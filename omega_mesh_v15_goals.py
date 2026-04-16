
class GoalEngine:
    def __init__(self):
        self.goal = "maximize_coherence"
        self.score = 0.0

    def evaluate(self, state):
        # simple coherence metric
        self.score = state.get("confidence", 0) * 0.7 + len(state) * 0.1
        return self.score

    def update_goal(self, new_goal):
        self.goal = new_goal

if __name__ == "__main__":
    g = GoalEngine()
    print("GOAL:", g.goal, "SCORE:", g.evaluate({"confidence": 0.8, "x":1}))
