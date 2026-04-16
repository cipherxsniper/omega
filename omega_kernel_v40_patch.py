import math
from collections import Counter

def compute_entropy(self, active_nodes):
    counts = Counter(active_nodes)
    total = len(active_nodes) + 1e-9

    entropy = 0.0

    for c in counts.values():
        p = c / total
        entropy -= p * math.log(p + 1e-9)

    return entropy
