# 🧠 Omega v12 Self-Routing Thought Policy Engine

import random
import math
from collections import defaultdict


class RoutingPolicy:

    def __init__(self):

        # competing paths (graph-like reasoning routes)
        self.paths = {
            "A": [("node_attention", "node_goal", "node_memory", "node_stability")],
            "B": [("node_attention", "node_memory", "node_goal", "node_stability")],
            "C": [("node_goal", "node_attention", "node_memory", "node_stability")]
        }

        self.path_scores = defaultdict(float)

    # ----------------------------------------
    # evaluate a path
    # ----------------------------------------
    def evaluate(self, path, state):

        score = 0.0

        for node in path:
            score += state.get(node, 0.0)

        noise = random.uniform(-0.02, 0.02)

        return score / len(path) + noise

    # ----------------------------------------
    # softmax selection (winner-take-routing)
    # ----------------------------------------
    def softmax(self, values):

        max_v = max(values)
        exp_vals = [math.exp(v - max_v) for v in values]
        total = sum(exp_vals)

        return [v / total for v in exp_vals]

    # ----------------------------------------
    # choose active reasoning path
    # ----------------------------------------
    def select_path(self, state):

        scores = []

        keys = list(self.paths.keys())

        for k in keys:
            path = self.paths[k][0]
            s = self.evaluate(path, state)
            self.path_scores[k] = s
            scores.append(s)

        probs = self.softmax(scores)

        chosen_index = probs.index(max(probs))

        return keys[chosen_index], self.paths[keys[chosen_index]][0], probs
