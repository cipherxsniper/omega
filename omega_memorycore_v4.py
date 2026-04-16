import math
from collections import defaultdict, deque
import random


class OmegaMemoryCoreV4:
    def __init__(self, max_stm=200):
        # -----------------------------
        # MEMORY LAYERS
        # -----------------------------
        self.stm = deque(maxlen=max_stm)        # short-term raw states
        self.ltm = defaultdict(int)             # compressed frequency memory
        self.patterns = defaultdict(int)        # signature frequency map
        self.anomalies = []

        # -----------------------------
        # PREDICTION LAYER (NEW)
        # -----------------------------
        # transition: state_signature -> next_state_signature -> count
        self.transitions = defaultdict(lambda: defaultdict(int))

        self.last_signature = None
        self.last_state = None

        self.tick_count = 0

    # =========================================================
    # INGESTION
    # =========================================================
    def ingest(self, state: dict):
        self.stm.append(state)
        self.tick_count += 1

        signature = self.compress(state)

        self.patterns[signature] += 1
        self.ltm[signature] += 1

        self._detect_anomaly(state)

        # -----------------------------
        # LEARN TRANSITION (KEY UPGRADE)
        # -----------------------------
        if self.last_signature is not None:
            self.transitions[self.last_signature][signature] += 1

        self.last_signature = signature
        self.last_state = state

        if self.tick_count % 10 == 0:
            self.consolidate()

    # =========================================================
    # STATE COMPRESSION
    # =========================================================
    def compress(self, state):
        e_bin = round(state.get("entropy", 0), 1)
        s_bin = round(state.get("stability", 0), 1)
        n_bin = int(state.get("nodes", 0) / 5) * 5
        return f"E{e_bin}_S{s_bin}_N{n_bin}"

    # =========================================================
    # CONSOLIDATION
    # =========================================================
    def consolidate(self):
        for state in list(self.stm):
            sig = self.compress(state)
            self.ltm[sig] += 1

    # =========================================================
    # ANOMALY DETECTION
    # =========================================================
    def _detect_anomaly(self, state):
        if not self.last_state:
            return

        e_delta = abs(state["entropy"] - self.last_state["entropy"])
        s_delta = abs(state["stability"] - self.last_state["stability"])

        if e_delta > 0.4 or s_delta > 0.4:
            self.anomalies.append({
                "state": state,
                "e_delta": e_delta,
                "s_delta": s_delta,
                "tick": self.tick_count
            })

    # =========================================================
    # 🔮 PREDICTION ENGINE (NEW CORE FEATURE)
    # =========================================================
    def predict_next(self, current_state: dict):
        current_sig = self.compress(current_state)

        if current_sig not in self.transitions:
            return {
                "prediction": None,
                "confidence": 0.0
            }

        next_map = self.transitions[current_sig]

        # find most likely next state
        best_sig = max(next_map.items(), key=lambda x: x[1])[0]
        total = sum(next_map.values())

        confidence = next_map[best_sig] / total if total > 0 else 0

        return {
            "prediction": self._decode_signature(best_sig),
            "signature": best_sig,
            "confidence": round(confidence, 4)
        }

    # =========================================================
    # SIGNATURE DECODER (APPROXIMATE RECONSTRUCTION)
    # =========================================================
    def _decode_signature(self, sig: str):
        # E0.3_S0.7_N10
        try:
            parts = sig.split("_")
            e = float(parts[0][1:])
            s = float(parts[1][1:])
            n = int(parts[2][1:])
            return {
                "entropy": e,
                "stability": s,
                "nodes": n
            }
        except:
            return None

    # =========================================================
    # INSIGHT ENGINE
    # =========================================================
    def get_dominant_patterns(self, top_k=5):
        return sorted(
            self.patterns.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

    def get_anomaly_rate(self):
        return len(self.anomalies) / self.tick_count if self.tick_count else 0

    def get_memory_snapshot(self):
        return {
            "stm_size": len(self.stm),
            "ltm_size": len(self.ltm),
            "patterns": len(self.patterns),
            "transitions": len(self.transitions),
            "anomalies": len(self.anomalies),
            "anomaly_rate": self.get_anomaly_rate()
        }


# =========================================================
# EXAMPLE USAGE
# =========================================================
if __name__ == "__main__":
    core = OmegaMemoryCoreV4()

    for i in range(100):
        state = {
            "entropy": math.sin(i / 6) + 0.5,
            "stability": math.cos(i / 8) + 0.5,
            "nodes": i % 25
        }

        core.ingest(state)

        if i > 10:
            prediction = core.predict_next(state)
            print("PRED:", prediction)

    print(core.get_memory_snapshot())
    print(core.get_dominant_patterns())
