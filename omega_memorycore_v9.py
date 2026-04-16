import math
from collections import defaultdict, deque

class OmegaMemoryCoreV9:
    def __init__(self, max_stm=200):

        self.stm = deque(maxlen=max_stm)

        # clustered long-term memory (IMPORTANT FIX)
        self.ltm = defaultdict(int)

        # transition graph (now stable keys)
        self.transitions = defaultdict(lambda: defaultdict(int))

        self.last_state = None
        self.tick = 0

    # -------------------------
    # 🔥 FIXED DISCRETIZATION LAYER
    # -------------------------
    def cluster_state(self, state):
        e = round(state.get("entropy", 0) * 2) / 2   # bucket size 0.5
        s = round(state.get("stability", 0) * 2) / 2 # bucket size 0.5
        n = int(state.get("nodes", 0) / 5) * 5

        return f"E{e}_S{s}_N{n}"

    # -------------------------
    # INGESTION
    # -------------------------
    def ingest(self, state):
        self.tick += 1
        self.stm.append(state)

        key = self.cluster_state(state)

        # memory accumulation
        self.ltm[key] += 1

        # transition learning
        if self.last_state:
            prev = self.cluster_state(self.last_state)
            self.transitions[prev][key] += 1

        self.last_state = state

    # -------------------------
    # 🔥 FIXED PREDICTION ENGINE
    # -------------------------
    def predict_next(self):
        if not self.last_state:
            return {"prediction": None, "confidence": 0.0}

        key = self.cluster_state(self.last_state)

        options = self.transitions.get(key, {})

        if not options:
            return {"prediction": None, "confidence": 0.0}

        # weighted selection
        total = sum(options.values())
        best = max(options.items(), key=lambda x: x[1])

        confidence = best[1] / total if total > 0 else 0.0

        return {
            "prediction": best[0],
            "confidence": round(confidence, 4)
        }

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "stm": len(self.stm),
            "ltm": len(self.ltm),
            "transitions": sum(len(v) for v in self.transitions.values()),
            "tick": self.tick
        }


# -------------------------
# TEST
# -------------------------
if __name__ == "__main__":
    import math

    core = OmegaMemoryCoreV9()

    for i in range(100):

        core.ingest({
            "entropy": math.sin(i / 6),
            "stability": math.cos(i / 7),
            "nodes": i % 25
        })

        if i % 10 == 0:
            print(core.snapshot())
            print(core.predict_next())
