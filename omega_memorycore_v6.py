import math
import time
from collections import deque, defaultdict


class OmegaMemoryCoreV6:
    def __init__(self, max_stm=200):
        # Short-term memory stream
        self.stm = deque(maxlen=max_stm)

        # Long-term memory compression
        self.ltm = defaultdict(int)

        # Pattern tracking
        self.patterns = defaultdict(int)

        # Cognitive chain (THIS FIXES YOUR EMPTY OUTPUT)
        self.chain = deque(maxlen=500)

        # Transitions between states
        self.transitions = deque(maxlen=500)

        # Anomaly log
        self.anomalies = []

        # Attention system (weights importance of signals)
        self.attention = {
            "entropy": 1.0,
            "stability": 1.0,
            "nodes": 1.0
        }

        # State tracking
        self.last_state = None

        # Confidence (dynamic, NOT fixed)
        self.confidence = 0.5

        # Tick counter
        self.tick = 0

    # -----------------------------
    # INGESTION PIPELINE
    # -----------------------------
    def ingest(self, state: dict):
        self.stm.append(state)
        self.tick += 1

        self._update_attention(state)
        self._detect_anomaly(state)
        self._track_pattern(state)

        if self.last_state is not None:
            transition = self._compute_transition(self.last_state, state)
            self.transitions.append(transition)
            self._build_thought_chain(state, transition)

        self._update_confidence(state)

        self.last_state = state

        if self.tick % 10 == 0:
            self.consolidate()

    # -----------------------------
    # ATTENTION SYSTEM
    # -----------------------------
    def _update_attention(self, state):
        # adaptive weighting based on volatility
        e = abs(state.get("entropy", 0))
        s = abs(state.get("stability", 0))

        self.attention["entropy"] = 0.9 * self.attention["entropy"] + 0.1 * e
        self.attention["stability"] = 0.9 * self.attention["stability"] + 0.1 * s

    # -----------------------------
    # TRANSITION ENGINE
    # -----------------------------
    def _compute_transition(self, prev, curr):
        e_delta = curr.get("entropy", 0) - prev.get("entropy", 0)
        s_delta = curr.get("stability", 0) - prev.get("stability", 0)
        n_delta = curr.get("nodes", 0) - prev.get("nodes", 0)

        direction = (
            "expanding" if e_delta > 0 else
            "contracting" if e_delta < 0 else
            "stable"
        )

        return {
            "e_delta": e_delta,
            "s_delta": s_delta,
            "n_delta": n_delta,
            "direction": direction,
            "tick": self.tick
        }

    # -----------------------------
    # THINKING / CHAIN BUILDER (CORE FIX)
    # -----------------------------
    def _build_thought_chain(self, state, transition):
        confidence_delta = 1.0 - min(1.0, abs(transition["e_delta"]) + abs(transition["s_delta"]))

        node = {
            "tick": self.tick,
            "state": state,
            "transition": transition,
            "confidence": confidence_delta,
            "pattern": self._compress(state)
        }

        self.chain.append(node)

    # -----------------------------
    # CONFIDENCE ENGINE
    # -----------------------------
    def _update_confidence(self, state):
        volatility = abs(state.get("entropy", 0)) + abs(state.get("stability", 0))

        decay = 0.95 if volatility > 1.2 else 1.02

        self.confidence *= decay
        self.confidence = max(0.05, min(self.confidence, 1.0))

    # -----------------------------
    # ANOMALY DETECTOR
    # -----------------------------
    def _detect_anomaly(self, state):
        if not self.last_state:
            return

        e_delta = abs(state["entropy"] - self.last_state["entropy"])
        s_delta = abs(state["stability"] - self.last_state["stability"])

        if e_delta > 0.5 or s_delta > 0.5:
            self.anomalies.append({
                "state": state,
                "e_delta": e_delta,
                "s_delta": s_delta,
                "tick": self.tick
            })

    # -----------------------------
    # PATTERN TRACKING
    # -----------------------------
    def _track_pattern(self, state):
        key = self._compress(state)
        self.patterns[key] += 1

    # -----------------------------
    # MEMORY COMPRESSION
    # -----------------------------
    def _compress(self, state):
        e = round(state.get("entropy", 0), 2)
        s = round(state.get("stability", 0), 2)
        n = int(state.get("nodes", 0) / 5) * 5
        return f"E{e}_S{s}_N{n}"

    # -----------------------------
    # CONSOLIDATION (STM → LTM)
    # -----------------------------
    def consolidate(self):
        for state in list(self.stm):
            key = self._compress(state)
            self.ltm[key] += 1

    # -----------------------------
    # INSIGHTS ENGINE
    # -----------------------------
    def get_dominant_patterns(self, top_k=5):
        return sorted(self.patterns.items(), key=lambda x: x[1], reverse=True)[:top_k]

    def get_memory_snapshot(self):
        return {
            "stm": len(self.stm),
            "ltm": len(self.ltm),
            "patterns": len(self.patterns),
            "transitions": len(self.transitions),
            "anomalies": len(self.anomalies),
            "chain_length": len(self.chain),
            "confidence": round(self.confidence, 4)
        }

    def get_latest_thoughts(self, n=5):
        return list(self.chain)[-n:]


# -----------------------------
# TEST RUN
# -----------------------------
if __name__ == "__main__":
    core = OmegaMemoryCoreV6()

    for i in range(50):
        core.ingest({
            "entropy": math.sin(i / 5) + 0.5,
            "stability": math.cos(i / 7) + 0.5,
            "nodes": i % 20
        })

        time.sleep(0.05)

    print(core.get_memory_snapshot())
    print(core.get_dominant_patterns())
    print(core.get_latest_thoughts())
