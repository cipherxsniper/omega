import math
import random
from collections import deque, defaultdict


class OmegaMemoryCoreV11:
    def __init__(self, max_stm=200):
        self.stm = deque(maxlen=max_stm)
        self.ltm = defaultdict(float)
        self.patterns = defaultdict(float)

        self.chain = []
        self.transitions = []
        self.predictions = []
        self.anomalies = []

        self.beliefs = defaultdict(float)
        self.attention = defaultdict(float)

        self.last_state = None
        self.tick = 0

        # recursive cognition knobs
        self.anomaly_threshold = 0.5

    # -------------------------
    # INGESTION (WITH FEEDBACK LOOP)
    # -------------------------
    def ingest(self, state: dict, feedback_weight=1.0):

        # inject prediction feedback into reality stream
        if self.predictions:
            last_pred = self.predictions[-1]
            state = {
                "entropy": state["entropy"] + (last_pred["entropy"] - state["entropy"]) * 0.1,
                "stability": state["stability"] + (last_pred["stability"] - state["stability"]) * 0.1,
                "nodes": state["nodes"]
            }

        self.stm.append(state)
        self.tick += 1

        self._update_patterns(state, feedback_weight)
        self._attention(state)
        self._transition(state)
        self._belief_update(state)
        self._predict(state)

        self._self_adapt()

        self.last_state = state

    # -------------------------
    # COMPRESSION
    # -------------------------
    def compress(self, state):
        return (
            round(state["entropy"], 2),
            round(state["stability"], 2),
            int(state["nodes"] / 5)
        )

    # -------------------------
    # PATTERNS (SELF-WEIGHTING)
    # -------------------------
    def _update_patterns(self, state, w):
        key = self.compress(state)
        self.patterns[key] += w

    # -------------------------
    # ATTENTION
    # -------------------------
    def _attention(self, state):
        score = abs(state["entropy"]) + abs(state["stability"])
        self.attention[self.tick] = score

    # -------------------------
    # TRANSITION + ANOMALY LEARNING
    # -------------------------
    def _transition(self, state):
        if not self.last_state:
            return

        e_delta = state["entropy"] - self.last_state["entropy"]
        s_delta = state["stability"] - self.last_state["stability"]

        transition = {
            "tick": self.tick,
            "e_delta": e_delta,
            "s_delta": s_delta
        }

        self.transitions.append(transition)
        self.chain.append(transition)

        # adaptive anomaly detection
        score = abs(e_delta) + abs(s_delta)

        if score > self.anomaly_threshold:
            self.anomalies.append(transition)
            self.anomaly_threshold *= 0.99  # learns tolerance

    # -------------------------
    # BELIEF SYSTEM (SELF-REWRITING)
    # -------------------------
    def _belief_update(self, state):
        key = self.compress(state)
        influence = self.patterns[key] * 0.01
        self.beliefs[key] += influence

        # belief decay + normalization
        for k in self.beliefs:
            self.beliefs[k] *= 0.999

    # -------------------------
    # PREDICTION ENGINE
    # -------------------------
    def _predict(self, state):
        if len(self.stm) < 3:
            return

        prev = list(self.stm)[-2]

        pred = {
            "tick": self.tick + 1,
            "entropy": state["entropy"] + (state["entropy"] - prev["entropy"]),
            "stability": state["stability"] + (state["stability"] - prev["stability"]),
        }

        self.predictions.append(pred)

    # -------------------------
    # SELF-ADAPTATION LOOP
    # -------------------------
    def _self_adapt(self):
        # pattern reinforcement
        for k in self.patterns:
            self.patterns[k] *= 0.999

        # belief influence modifies pattern sensitivity
        dominant = max(self.beliefs.items(), key=lambda x: x[1], default=None)
        if dominant:
            self.anomaly_threshold += (dominant[1] * 0.0001)
            self.anomaly_threshold = max(0.1, min(1.5, self.anomaly_threshold))

    # -------------------------
    # CONSOLIDATION
    # -------------------------
    def consolidate(self):
        for state in self.stm:
            key = self.compress(state)
            self.ltm[key] += 1

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "tick": self.tick,
            "stm": len(self.stm),
            "ltm": len(self.ltm),
            "beliefs": len(self.beliefs),
            "patterns": len(self.patterns),
            "anomalies": len(self.anomalies),
            "threshold": self.anomaly_threshold
        }


# -------------------------
# TEST LOOP
# -------------------------
if __name__ == "__main__":
    core = OmegaMemoryCoreV11()

    for i in range(80):
        core.ingest({
            "entropy": math.sin(i / 4) + random.uniform(-0.2, 0.2),
            "stability": math.cos(i / 5) + random.uniform(-0.2, 0.2),
            "nodes": i % 30
        })

        if i % 10 == 0:
            print(core.snapshot())
