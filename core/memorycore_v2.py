# core/memorycore_v2.py

import time

class MemoryCore:
    def __init__(self, shared_state):
        self.state = shared_state

    def store(self, data, tag="general"):
        entry = {
            "time": time.time(),
            "tag": tag,
            "data": data
        }

        self.state["memory"].append(entry)

    def retrieve(self, tag=None, limit=20):
        data = self.state["memory"][-limit:]
        if tag:
            data = [d for d in data if d["tag"] == tag]
        return data

    def importance_score(self, data):
        score = 0
        if "integrate" in str(data): score += 2
        if "reinforce" in str(data): score += 3
        if "error" in str(data): score -= 2
        return score
