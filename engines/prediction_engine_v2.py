# engines/prediction_engine_v2.py

import random

class PredictionEngine:
    def __init__(self, shared_state):
        self.state = shared_state

    def predict(self):
        result = random.choice(["UP", "DOWN", "STABLE"])
        self.state["predictions"].append(result)
        return result
