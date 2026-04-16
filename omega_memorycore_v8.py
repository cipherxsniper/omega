import math
import time
from collections import defaultdict, deque

class OmegaMemoryCoreV8:
    def __init__(self, max_stm=200):
        # short-term memory
        self.stm = deque(maxlen=max_stm)

        # long-term compressed memory
        self.ltm = defaultdict(float)

        # pattern confidence memory
        self.beliefs = defaultdict(lambda: 0.5)

        # transition memory (sequence learning)
        self.transitions = defaultdict(lambda: defaultdict(int))

        self.anomalies = []

        self.last_state = None
        self.tick = 0

    # -------------------------
    # INGESTION
    # -------------------------
    def ingest(self, state: dict):
        self.stm.append(state)
        self.tick += 1

        if self.last_state:
            self._learn_transition(self.last_state, state)
            self._detect_anomaly(state)

        self._update_beliefs(state)

        if self.tick % 10 == 0:
            self._consolidate()

        self.last_state = state

    # -------------------------
    # COMPRESSION
    # -------------------------
    def compress(self, state):
        e = round(state.get("entropy", 0), 1)
        s = round(state.get("stability", 0), 1)
        n = int(state.get("nodes", 0) / 5) * 5
        return f"E{e}_S{s}_N{n}"

    # -------------------------
    # TRANSITION LEARNING
    # -------------------------
    def _learn_transition(self, prev, curr):
        a = self.compress(prev)
        b = self.compress(curr)
        self.transitions[a][b] += 1

    # -------------------------
    # BELIEF UPDATES (CORE UPGRADE)
    # -------------------------
    def _update_beliefs(self, state):
        key = self.compress(state)

        # reinforcement learning style update
        prev = self.beliefs[key]
        reward = 1.0 / (1.0 + abs(state.get("entropy", 0)))

        self.beliefs[key] = (prev * 0.9) + (reward * 0.1)

    # -------------------------
    # ANOMALY DETECTION
    # -------------------------
    def _detect_anomaly(self, state):
        e = state.get("entropy", 0)
        s = state.get("stability", 0)

        if abs(e) > 0.9 or abs(s) > 0.9:
            self.anomalies.append({
                "tick": self.tick,
                "state": state
            })

    # -------------------------
    # CONSOLIDATION + DECAY
    # -------------------------
    def _consolidate(self):
        for s in self.stm:
            k = self.compress(s)
            self.ltm[k] += 1

        # decay weak memories
        for k in list(self.ltm.keys()):
            self.ltm[k] *= 0.98
            if self.ltm[k] < 0.1:
                del self.ltm[k]

    # -------------------------
    # PREDICTION ENGINE (FIXED)
    # -------------------------
    def predict_next(self):
        if not self.last_state:
            return {"prediction": None, "confidence": 0.0}

        key = self.compress(self.last_state)
        options = self.transitions.get(key, {})

        if not options:
            return {"prediction": None, "confidence": 0.0}

        best = max(options.items(), key=lambda x: x[1])

        confidence = min(1.0, best[1] / (sum(options.values()) + 1e-6))

        return {
            "prediction": best[0],
            "confidence": confidence
        }

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "stm": len(self.stm),
            "ltm": len(self.ltm),
            "beliefs": len(self.beliefs),
            "transitions": sum(len(v) for v in self.transitions.values()),
            "anomalies": len(self.anomalies),
            "tick": self.tick
        }


# -------------------------
# TEST RUN
# -------------------------
if __name__ == "__main__":
    core = OmegaMemoryCoreV8()

    for i in range(80):
        core.ingest({
            "entropy": math.sin(i / 6),
            "stability": math.cos(i / 7),
            "nodes": i % 25
        })

        if i % 10 == 0:
            print(core.snapshot())
            print(core.predict_next())
