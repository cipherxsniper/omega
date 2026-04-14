# engines/learning_engine_v17.py

class LearningEngine:
    def __init__(self):
        self.knowledge = {}

    def learn(self, input_data):
        key = str(input_data)
        self.knowledge[key] = self.knowledge.get(key, 0) + 1
        return f"[Learning] Learned pattern: {key}"

    def predict_next(self):
        if not self.knowledge:
            return None
        return max(self.knowledge, key=self.knowledge.get)

    def evolve(self):
        return {
            "known_patterns": len(self.knowledge),
            "top_pattern": self.predict_next()
        }
