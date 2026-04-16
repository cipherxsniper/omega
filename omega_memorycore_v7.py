import math
import time
import random
from collections import deque, defaultdict


class OmegaMemoryCoreV7:
    """
    MEMORYCORE V7–V9 STACKED COGNITION SYSTEM
    """

    def __init__(self, max_stm=200):

        # ---------------- V1 CORE ----------------
        self.stm = deque(maxlen=max_stm)
        self.ltm = defaultdict(int)

        # ---------------- V2 PATTERNS ----------------
        self.patterns = defaultdict(int)

        # ---------------- V3 ANOMALIES ----------------
        self.anomalies = []

        # ---------------- V5 COGNITIVE CHAIN ----------------
        self.chain = deque(maxlen=1000)

        # ---------------- V6 TRANSITIONS ----------------
        self.transitions = deque(maxlen=1000)

        # ---------------- V6 ATTENTION ----------------
        self.attention = {
            "entropy": 1.0,
            "stability": 1.0,
            "nodes": 1.0
        }

        # ---------------- CORE STATE ----------------
        self.last_state = None
        self.tick = 0
        self.confidence = 0.5

        # ---------------- V8 PREDICTION ENGINE ----------------
        self.predictions = deque(maxlen=200)

        # ---------------- V9 META LAYER ----------------
        self.self_reflection_log = deque(maxlen=200)

    # =========================================================
    # INGESTION PIPELINE (ALL VERSIONS ACTIVE HERE)
    # =========================================================
    def ingest(self, state: dict):
        self.stm.append(state)
        self.tick += 1

        # V2 / V3 / V4
        self._track_pattern(state)
        self._detect_anomaly(state)

        # V6 attention update
        self._update_attention(state)

        # V5/V6 transition logic
        if self.last_state:
            transition = self._transition(self.last_state, state)
            self.transitions.append(transition)

            # V5 chain building
            self._build_chain(state, transition)

        # V8 prediction
        self._predict_next(state)

        # V9 self reflection
        if self.tick % 10 == 0:
            self._self_reflect()

        # V1/V4 consolidation
        if self.tick % 10 == 0:
            self.consolidate()

        # V7 adaptive confidence
        self._update_confidence(state)

        self.last_state = state

    # =========================================================
    # V2 / V4 PATTERN ENGINE
    # =========================================================
    def _compress(self, state):
        return (
            round(state.get("entropy", 0), 2),
            round(state.get("stability", 0), 2),
            state.get("nodes", 0) // 5
        )

    def _track_pattern(self, state):
        key = self._compress(state)
        self.patterns[key] += 1

    # =========================================================
    # V3 ANOMALY ENGINE
    # =========================================================
    def _detect_anomaly(self, state):
        if not self.last_state:
            return

        e = abs(state["entropy"] - self.last_state["entropy"])
        s = abs(state["stability"] - self.last_state["stability"])

        if e > 0.5 or s > 0.5:
            self.anomalies.append({
                "state": state,
                "delta": (e, s),
                "tick": self.tick
            })

    # =========================================================
    # V6 ATTENTION SYSTEM
    # =========================================================
    def _update_attention(self, state):
        self.attention["entropy"] = 0.9 * self.attention["entropy"] + 0.1 * abs(state["entropy"])
        self.attention["stability"] = 0.9 * self.attention["stability"] + 0.1 * abs(state["stability"])

    # =========================================================
    # V5 TRANSITION ENGINE
    # =========================================================
    def _transition(self, prev, curr):
        e = curr["entropy"] - prev["entropy"]
        s = curr["stability"] - prev["stability"]

        return {
            "e_delta": e,
            "s_delta": s,
            "direction": "expanding" if e > 0 else "contracting",
            "tick": self.tick
        }

    # =========================================================
    # V5 COGNITIVE CHAIN ENGINE (FIXED)
    # =========================================================
    def _build_chain(self, state, transition):
        node = {
            "tick": self.tick,
            "state": state,
            "transition": transition,
            "confidence": 1.0 - min(1.0, abs(transition["e_delta"]) + abs(transition["s_delta"]))
        }
        self.chain.append(node)

    # =========================================================
    # V7 CONFIDENCE SYSTEM (DYNAMIC)
    # =========================================================
    def _update_confidence(self, state):
        volatility = abs(state["entropy"]) + abs(state["stability"])

        if volatility > 1.2:
            self.confidence *= 0.95
        else:
            self.confidence *= 1.02

        self.confidence = max(0.05, min(self.confidence, 1.0))

    # =========================================================
    # V4 LTM CONSOLIDATION
    # =========================================================
    def consolidate(self):
        for s in list(self.stm):
            key = self._compress(s)
            self.ltm[key] += 1

    # =========================================================
    # V8 PREDICTION ENGINE
    # =========================================================
    def _predict_next(self, state):
        if not self.last_state:
            return

        prediction = {
            "tick": self.tick,
            "expected_entropy": state["entropy"] * random.uniform(0.95, 1.05),
            "expected_stability": state["stability"] * random.uniform(0.95, 1.05)
        }

        self.predictions.append(prediction)

    # =========================================================
    # V9 SELF-REFLECTION ENGINE
    # =========================================================
    def _self_reflect(self):
        reflection = {
            "tick": self.tick,
            "memory_load": len(self.stm),
            "pattern_diversity": len(self.patterns),
            "anomaly_rate": len(self.anomalies) / (self.tick + 1),
            "confidence": self.confidence
        }

        self.self_reflection_log.append(reflection)

        # meta-adjustment (V9 behavior)
        if reflection["anomaly_rate"] > 0.3:
            self.confidence *= 0.9

    # =========================================================
    # INSIGHTS
    # =========================================================
    def snapshot(self):
        return {
            "stm": len(self.stm),
            "ltm": len(self.ltm),
            "patterns": len(self.patterns),
            "anomalies": len(self.anomalies),
            "chain": len(self.chain),
            "transitions": len(self.transitions),
            "predictions": len(self.predictions),
            "confidence": round(self.confidence, 4)
        }

    def latest_thoughts(self, n=5):
        return list(self.chain)[-n:]

    def reflections(self, n=5):
        return list(self.self_reflection_log)[-n:]


# =========================================================
# TEST RUN
# =========================================================
if __name__ == "__main__":
    core = OmegaMemoryCoreV7()

    for i in range(60):
        core.ingest({
            "entropy": math.sin(i / 5) + 0.5,
            "stability": math.cos(i / 7) + 0.5,
            "nodes": i % 20
        })

        time.sleep(0.03)

    print(core.snapshot())
    print(core.latest_thoughts())
    print(core.reflections())
