import math
from collections import deque, defaultdict


class OmegaMemoryCoreV10:
    def __init__(self, max_stm=200):
        self.stm = deque(maxlen=max_stm)
        self.ltm = defaultdict(int)
        self.patterns = defaultdict(int)

        self.chain = []
        self.transitions = []
        self.predictions = []
        self.anomalies = []

        self.beliefs = defaultdict(float)
        self.attention = defaultdict(float)

        self.last_state = None
        self.tick = 0

    # -------------------------
    # INGESTION PIPELINE
    # -------------------------
    def ingest(self, state: dict):
        self.stm.append(state)
        self.tick += 1

        self._update_patterns(state)
        self._attention_score(state)
        self._transition(state)
        self._belief_update(state)
        self._predict(state)

        if self.tick % 10 == 0:
            self.consolidate()

        self.last_state = state

    # -------------------------
    # COMPRESSION ENGINE
    # -------------------------
    def compress(self, state):
        e = round(state.get("entropy", 0), 2)
        s = round(state.get("stability", 0), 2)
        n = int(state.get("nodes", 0) / 5) * 5
        return f"E{e}_S{s}_N{n}"

    # -------------------------
    # PATTERN TRACKING
    # -------------------------
    def _update_patterns(self, state):
        key = self.compress(state)
        self.patterns[key] += 1

    # -------------------------
    # ATTENTION MODEL
    # -------------------------
    def _attention_score(self, state):
        score = abs(state.get("entropy", 0)) + abs(state.get("stability", 0))
        self.attention[self.tick] = score

    # -------------------------
    # TRANSITION ENGINE
    # -------------------------
    def _transition(self, state):
        if not self.last_state:
            return

        e_delta = state["entropy"] - self.last_state["entropy"]
        s_delta = state["stability"] - self.last_state["stability"]

        direction = "expanding" if e_delta > 0 else "contracting"

        transition = {
            "tick": self.tick,
            "e_delta": e_delta,
            "s_delta": s_delta,
            "direction": direction
        }

        self.transitions.append(transition)

        self.chain.append({
            "tick": self.tick,
            "state": state,
            "transition": transition,
            "confidence": self._confidence(e_delta, s_delta)
        })

        if abs(e_delta) > 0.5 or abs(s_delta) > 0.5:
            self.anomalies.append(transition)

    # -------------------------
    # CONFIDENCE MODEL
    # -------------------------
    def _confidence(self, e_delta, s_delta):
        base = 1.0 - (abs(e_delta) + abs(s_delta)) / 2.0
        decay = math.exp(-len(self.anomalies) * 0.01)
        return max(0.0, min(1.0, base * decay))

    # -------------------------
    # BELIEF SYSTEM
    # -------------------------
    def _belief_update(self, state):
        key = self.compress(state)
        self.beliefs[key] += 0.05

    # -------------------------
    # PREDICTION ENGINE
    # -------------------------
    def _predict(self, state):
        if len(self.stm) < 3:
            return

        prev = list(self.stm)[-2]
        curr = state

        pred = {
            "tick": self.tick + 1,
            "entropy": curr["entropy"] + (curr["entropy"] - prev["entropy"]),
            "stability": curr["stability"] + (curr["stability"] - prev["stability"]),
        }

        self.predictions.append(pred)

    # -------------------------
    # CONSOLIDATION
    # -------------------------
    def consolidate(self):
        for state in list(self.stm):
            key = self.compress(state)
            self.ltm[key] += 1

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "stm": len(self.stm),
            "ltm": len(self.ltm),
            "beliefs": len(self.beliefs),
            "transitions": len(self.transitions),
            "anomalies": len(self.anomalies),
            "chain": len(self.chain),
            "tick": self.tick
        }

    # -------------------------
    # INSIGHT ENGINE
    # -------------------------
    def top_patterns(self, k=5):
        return sorted(self.patterns.items(), key=lambda x: x[1], reverse=True)[:k]

    def recent_chain(self, n=5):
        return self.chain[-n:]


if __name__ == "__main__":
    core = OmegaMemoryCoreV10()

    for i in range(60):
        core.ingest({
            "entropy": math.sin(i / 6),
            "stability": math.cos(i / 8),
            "nodes": i % 25
        })

        print(core.snapshot())
