import math
from collections import defaultdict, deque


class OmegaMemoryCoreV5:
    def __init__(self, max_stm=300):
        # -----------------------------
        # MEMORY SYSTEMS
        # -----------------------------
        self.stm = deque(maxlen=max_stm)
        self.ltm = defaultdict(int)
        self.patterns = defaultdict(int)
        self.anomalies = []

        # -----------------------------
        # LEARNING SYSTEMS
        # -----------------------------
        # transitions with weights
        self.transitions = defaultdict(lambda: defaultdict(float))

        # reward memory per state signature
        self.rewards = defaultdict(float)

        # attention weights (what system focuses on)
        self.attention = defaultdict(float)

        self.last_sig = None
        self.last_state = None

        self.tick = 0

        # goal bias (emergent direction pressure)
        self.goal_vector = {
            "low_entropy": 0.5,
            "high_stability": 0.5
        }

    # =========================================================
    # INGESTION
    # =========================================================
    def ingest(self, state: dict):
        self.stm.append(state)
        self.tick += 1

        sig = self.compress(state)

        self.patterns[sig] += 1
        self.ltm[sig] += 1

        self._update_attention(sig)
        self._detect_anomaly(state)

        # -----------------------------
        # LEARN TRANSITIONS (WEIGHTED)
        # -----------------------------
        if self.last_sig:
            reward = self._compute_reward(state)

            # strengthen or weaken transition
            self.transitions[self.last_sig][sig] += reward

        self.last_sig = sig
        self.last_state = state

        if self.tick % 15 == 0:
            self.consolidate()

    # =========================================================
    # STATE COMPRESSION
    # =========================================================
    def compress(self, state):
        e = round(state.get("entropy", 0), 2)
        s = round(state.get("stability", 0), 2)
        n = int(state.get("nodes", 0) / 5) * 5
        return f"E{e}_S{s}_N{n}"

    # =========================================================
    # REWARD FUNCTION (CORE INTELLIGENCE SHIFT)
    # =========================================================
    def _compute_reward(self, state):
        entropy = state.get("entropy", 0)
        stability = state.get("stability", 0)

        # goal pressure: low entropy + high stability
        reward = 0

        reward += (1.0 - entropy) * self.goal_vector["low_entropy"]
        reward += stability * self.goal_vector["high_stability"]

        # anomaly penalty
        if entropy > 0.8:
            reward -= 0.3

        return reward

    # =========================================================
    # ATTENTION SYSTEM (WHAT THE SYSTEM "CARES ABOUT")
    # =========================================================
    def _update_attention(self, sig):
        self.attention[sig] += 1

        # decay weak signals
        if len(self.attention) > 500:
            for k in list(self.attention.keys()):
                self.attention[k] *= 0.99

    # =========================================================
    # ANOMALY DETECTION
    # =========================================================
    def _detect_anomaly(self, state):
        if not self.last_state:
            return

        e_delta = abs(state["entropy"] - self.last_state["entropy"])
        s_delta = abs(state["stability"] - self.last_state["stability"])

        if e_delta > 0.45 or s_delta > 0.45:
            self.anomalies.append({
                "state": state,
                "tick": self.tick
            })

    # =========================================================
    # MULTI-STEP PREDICTION ENGINE (NEW)
    # =========================================================
    def predict_chain(self, state, steps=3):
        current = self.compress(state)
        chain = []
        confidence = 1.0

        for _ in range(steps):
            next_sig = self._best_next(current)

            if not next_sig:
                break

            next_state = self._decode(next_sig)
            chain.append(next_state)

            # decay confidence as uncertainty increases
            confidence *= self._transition_confidence(current, next_sig)

            current = next_sig

        return {
            "chain": chain,
            "confidence": round(confidence, 4)
        }

    # =========================================================
    # NEXT STATE SELECTION (REWARD-BIASED)
    # =========================================================
    def _best_next(self, sig):
        options = self.transitions.get(sig, {})
        if not options:
            return None

        return max(options.items(), key=lambda x: x[1])[0]

    def _transition_confidence(self, a, b):
        total = sum(self.transitions[a].values())
        if total == 0:
            return 0.0
        return self.transitions[a][b] / total

    # =========================================================
    # DECODER
    # =========================================================
    def _decode(self, sig):
        try:
            e, s, n = sig.split("_")
            return {
                "entropy": float(e[1:]),
                "stability": float(s[1:]),
                "nodes": int(n[1:])
            }
        except:
            return None

    # =========================================================
    # CONSOLIDATION
    # =========================================================
    def consolidate(self):
        for state in list(self.stm):
            sig = self.compress(state)
            self.ltm[sig] += 1

    # =========================================================
    # INSIGHTS
    # =========================================================
    def dominant_states(self, k=5):
        return sorted(
            self.patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]

    def most_attended(self, k=5):
        return sorted(
            self.attention.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]

    def snapshot(self):
        return {
            "stm": len(self.stm),
            "ltm": len(self.ltm),
            "patterns": len(self.patterns),
            "transitions": len(self.transitions),
            "anomalies": len(self.anomalies),
            "attention_nodes": len(self.attention)
        }


# =========================================================
# EXAMPLE RUN
# =========================================================
if __name__ == "__main__":
    import random

    core = OmegaMemoryCoreV5()

    for i in range(120):
        state = {
            "entropy": abs(math.sin(i / 7) + random.uniform(-0.1, 0.1)),
            "stability": abs(math.cos(i / 9) + random.uniform(-0.1, 0.1)),
            "nodes": i % 30
        }

        core.ingest(state)

        if i > 20:
            print(core.predict_chain(state, steps=4))

    print(core.snapshot())
    print(core.most_attended())
