import json
import time
import threading

class TruthMemory:
    """
    Single source of truth for ALL Omega nodes.
    Every node writes HERE. Nothing else is allowed to be final memory.
    """

    def __init__(self):
        self.memory = []
        self.lock = threading.Lock()

    def write(self, node, data):
        with self.lock:
            entry = {
                "timestamp": time.time(),
                "node": node,
                "data": data
            }
            self.memory.append(entry)

    def read_latest(self, n=10):
        return self.memory[-n:]

    def resolve_truth(self):
        """
        Collapses contradictions into dominant patterns.
        (simple version of consensus weighting)
        """
        summary = {}
        for m in self.memory:
            key = str(m["data"])
            summary[key] = summary.get(key, 0) + 1

        return sorted(summary.items(), key=lambda x: x[1], reverse=True)
