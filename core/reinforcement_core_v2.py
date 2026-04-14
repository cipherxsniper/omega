import random
import time

class ReinforcementCore:
    def __init__(self):
        self.score = 0
        self.history = []
        self.positive = 0
        self.negative = 0
        self.last_action = None
        self.last_result = None

    def evaluate(self, prediction):
        """
        Evaluate outcome of prediction
        """
        if prediction == "UP":
            reward = random.randint(1, 5)
            self.score += reward
            self.positive += 1
            result = "positive"

        elif prediction == "DOWN":
            penalty = random.randint(1, 5)
            self.score -= penalty
            self.negative += 1
            result = "negative"

        else:
            result = "neutral"

        self.last_result = result

        self.history.append({
            "time": time.time(),
            "prediction": prediction,
            "result": result,
            "score": self.score
        })

        return self.score

    def feedback(self, action):
        """
        Link action → result (learning cause/effect)
        """
        self.last_action = action

        if self.last_result == "positive":
            return f"[Reinforcement] Strengthen action → {action}"
        elif self.last_result == "negative":
            return f"[Reinforcement] Weaken action → {action}"
        else:
            return f"[Reinforcement] Neutral learning → {action}"

    def intelligence_trend(self):
        """
        🔥 THIS IS WHAT YOUR SYSTEM WAS MISSING
        Tracks intelligence growth
        """
        total = self.positive + self.negative

        if total == 0:
            ratio = 0
        else:
            ratio = self.positive / total

        return {
            "positive": self.positive,
            "negative": self.negative,
            "ratio": ratio,
            "score": self.score
        }

    def adaptive_adjustment(self):
        """
        Self-adjust learning behavior based on trend
        """
        trend = self.intelligence_trend()

        if trend["ratio"] < 0.4:
            return "[Adaptive] Learning unstable → exploring new strategies"

        elif trend["ratio"] > 0.7:
            return "[Adaptive] Strong intelligence growth → exploiting patterns"

        else:
            return "[Adaptive] Balanced learning state"
