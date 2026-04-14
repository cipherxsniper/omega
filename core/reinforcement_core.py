# core/reinforcement_core.py (UPGRADE)

class ReinforcementCore:
    def __init__(self):
        self.score = 0

    def evaluate(self, decision, data):
        reward = 0

        # 🧠 Reward useful behavior
        if "integrate" in decision.lower():
            reward += 2

        if "analyze" in decision.lower():
            reward += 1

        if "reinforce" in decision.lower():
            reward += 3

        # ❌ Penalize useless repetition
        if "idle" in decision.lower():
            reward -= 2

        # 🔥 Penalize low-value data
        if "No data" in str(data):
            reward -= 3

        self.score += reward
        return self.score

    def get_score(self):
        return self.score
