import random
import math
import copy

class OmegaSelfModelV23:
    def __init__(self):
        self.model_bias = {}
        self.prediction_history = []
        self.error_log = []
        self.step = 0

    # ---------------------------
    # PREDICT NEXT STATE
    # ---------------------------
    def predict(self, state):
        scores = state["scores"]

        # simple learned bias per brain
        predicted = {}

        total = sum(scores.values()) or 1.0

        for k, v in scores.items():
            bias = self.model_bias.get(k, 1.0)

            # prediction = weighted projection + bias drift
            predicted[k] = (v / total) * bias

        # normalize prediction
        s = sum(predicted.values()) or 1.0
        for k in predicted:
            predicted[k] /= s

        return predicted

    # ---------------------------
    # COMPARE PREDICTION VS REALITY
    # ---------------------------
    def compute_error(self, predicted, actual):
        error = 0.0

        for k in actual:
            error += abs(actual[k] - predicted.get(k, 0.0))

        return error

    # ---------------------------
    # UPDATE SELF MODEL
    # ---------------------------
    def learn(self, predicted, actual):
        for k in actual:
            err = actual[k] - predicted.get(k, 0.0)

            # adjust bias toward reality
            self.model_bias[k] = self.model_bias.get(k, 1.0) + (err * 0.1)

            # clamp stability
            self.model_bias[k] = max(0.1, min(3.0, self.model_bias[k]))

    # ---------------------------
    # MAIN STEP
    # ---------------------------
    def step_cycle(self, state):
        self.step += 1

        predicted = self.predict(state)

        actual = state["scores"]

        error = self.compute_error(predicted, actual)

        self.learn(predicted, actual)

        self.prediction_history.append(predicted)
        self.error_log.append(error)

        if len(self.error_log) > 200:
            self.error_log = self.error_log[-200:]

        return {
            "step": self.step,
            "predicted_top": max(predicted, key=predicted.get),
            "actual_top": state["top"],
            "error": error,
            "model_state": dict(self.model_bias)
        }
