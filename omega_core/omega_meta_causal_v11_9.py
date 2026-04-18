# 🧠 Omega v11.9 Meta-Causal Engine

import random
from collections import defaultdict

class MetaCausalEngine:

    def __init__(self):
        # edge -> history of influence
        self.edge_memory = defaultdict(list)

        # meta relationships (edge influencing edge)
        self.meta_edges = defaultdict(lambda: defaultdict(float))

    # -----------------------------------
    # record causal event
    # -----------------------------------
    def record(self, src, dst, signal):

        key = (src, dst)
        self.edge_memory[key].append(signal)

        # cap memory
        self.edge_memory[key] = self.edge_memory[key][-50:]

    # -----------------------------------
    # compute edge strength
    # -----------------------------------
    def edge_strength(self, src, dst):

        key = (src, dst)
        vals = self.edge_memory.get(key, [0.0])

        if not vals:
            return 0.0

        return sum(vals) / len(vals)

    # -----------------------------------
    # build meta causality (edge → edge)
    # -----------------------------------
    def build_meta(self):

        keys = list(self.edge_memory.keys())

        for i in range(len(keys)):
            for j in range(len(keys)):

                if i == j:
                    continue

                e1 = keys[i]
                e2 = keys[j]

                s1 = self.edge_strength(*e1)
                s2 = self.edge_strength(*e2)

                influence = abs(s1 - s2) * random.uniform(0.8, 1.2)

                self.meta_edges[e1][e2] = influence

    # -----------------------------------
    # dominant meta path
    # -----------------------------------
    def dominant_meta_path(self):

        best = None
        best_score = -1

        for src, targets in self.meta_edges.items():
            for dst, w in targets.items():

                if w > best_score:
                    best_score = w
                    best = (src, "→", dst, round(w, 3))

        return best
