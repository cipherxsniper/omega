# engines/prediction_engine.py

import random

class PredictionEngine:
    def __init__(self):
        self.history = []

    def simulate(self):
        scenarios = ["UP", "DOWN", "STABLE"]
        prediction = random.choice(scenarios)
        self.history.append(prediction)
        return prediction

    def confidence(self):
        if not self.history:
            return 0
        return self.history.count("UP") / len(self.history)

    def future_model(self):
        return {
            "history": self.history[-5:],
            "confidence_up": self.confidence()
        }
