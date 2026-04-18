# 🧠 OMEGA v9.3 - EVENT MEMORY LAYER
# ----------------------------------
# Adds temporal intelligence to nodes
# ----------------------------------

import time


class EventMemoryV9_3:

    def __init__(self):
        self.events = {}  # node → list of events

    def record(self, node, score, decision, risk):

        if node not in self.events:
            self.events[node] = []

        self.events[node].append({
            "t": time.time(),
            "score": score,
            "decision": decision,
            "risk": risk
        })

    def history(self, node):
        return self.events.get(node, [])


    def trend(self, node):

        history = self.history(node)

        if len(history) < 2:
            return "INSUFFICIENT_DATA"

        scores = [h["score"] for h in history[-10:]]

        delta = scores[-1] - scores[0]

        if delta > 0.05:
            return "IMPROVING"

        if delta < -0.05:
            return "DEGRADING"

        return "STABLE"


    def bias_score(self, node, base_score):

        history = self.history(node)

        if not history:
            return base_score

        last = history[-1]["score"]

        # mild reinforcement learning effect
        adjusted = (base_score * 0.7) + (last * 0.3)

        return max(0.0, min(1.0, adjusted))
