import random

class MoERouter:

    def route(self, brain_outputs):

        # soft competition (not hard max)
        total = sum(brain_outputs.values()) + 1e-6

        scores = {}

        for k, v in brain_outputs.items():
            scores[k] = v / total

        # winner influence (soft gating)
        winner = max(scores, key=scores.get)

        return winner, scores
