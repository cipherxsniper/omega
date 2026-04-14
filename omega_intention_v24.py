import math
import random

class OmegaIntentionV24:
    def __init__(self):
        self.intents = {
            "stability": 0.0,
            "exploration": 0.0,
            "convergence": 0.0,
            "diversity": 0.0
        }

        self.history = []
        self.step = 0

    # ---------------------------
    # UTILITY EVALUATION
    # ---------------------------
    def evaluate_utilities(self, state):
        scores = state["scores"]

        values = {}

        avg = sum(scores.values()) / len(scores)

        variance = max(scores.values()) - min(scores.values())

        # stability utility (low variance = good)
        values["stability"] = 1.0 / (1.0 + variance)

        # convergence utility (one dominant brain = strong)
        values["convergence"] = max(scores.values())

        # exploration utility (more spread = good)
        values["exploration"] = variance

        # diversity utility (inverse dominance)
        values["diversity"] = 1.0 - max(scores.values())

        return values

    # ---------------------------
    # INTENT FORMATION
    # ---------------------------
    def form_intent(self, utilities):
        # normalize utilities
        total = sum(abs(v) for v in utilities.values()) or 1.0

        for k in self.intents:
            self.intents[k] = utilities[k] / total

        # choose dominant intent
        dominant = max(self.intents, key=self.intents.get)

        return dominant, dict(self.intents)

    # ---------------------------
    # INTENT-AWARE DECISION TAGGING
    # ---------------------------
    def tag_prediction(self, predicted_state, dominant_intent):
        tag = {
            "predicted_top": max(predicted_state, key=predicted_state.get),
            "intent": dominant_intent
        }

        # intent influences interpretation
        if dominant_intent == "stability":
            tag["mode"] = "low_variance_lock"
        elif dominant_intent == "exploration":
            tag["mode"] = "high_entropy_search"
        elif dominant_intent == "convergence":
            tag["mode"] = "single_peak_focus"
        else:
            tag["mode"] = "distribution_preservation"

        return tag

    # ---------------------------
    # MAIN STEP
    # ---------------------------
    def step_cycle(self, state, predicted_state):
        self.step += 1

        utilities = self.evaluate_utilities(state)

        dominant_intent, intent_map = self.form_intent(utilities)

        tagged = self.tag_prediction(predicted_state, dominant_intent)

        self.history.append({
            "step": self.step,
            "intent": dominant_intent,
            "intent_map": intent_map,
            "tag": tagged
        })

        return {
            "step": self.step,
            "dominant_intent": dominant_intent,
            "intent_map": intent_map,
            "prediction_tag": tagged
        }
