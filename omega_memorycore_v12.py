import random
import math
from collections import deque, defaultdict

# -----------------------------
# SINGLE MEMORY CORE (NODE)
# -----------------------------
class MemoryCoreV12:
    def __init__(self, core_id, max_stm=50):
        self.core_id = core_id

        self.stm = deque(maxlen=max_stm)
        self.ltm = defaultdict(float)

        self.beliefs = defaultdict(float)
        self.predictions = deque(maxlen=20)

        self.tick = 0
        self.confidence = 1.0

    # -------------------------
    # INGESTION
    # -------------------------
    def ingest(self, state):
        self.stm.append(state)
        self.tick += 1

        self._update_beliefs(state)
        prediction = self._predict_next(state)

        self.predictions.append(prediction)

        # memory consolidation
        if self.tick % 5 == 0:
            self._consolidate()

        return prediction

    # -------------------------
    # BELIEF UPDATE (SELF-ADJUSTING GRAPH)
    # -------------------------
    def _update_beliefs(self, state):
        entropy = state.get("entropy", 0)
        stability = state.get("stability", 0)

        self.beliefs["entropy"] = self._smooth(self.beliefs["entropy"], entropy)
        self.beliefs["stability"] = self._smooth(self.beliefs["stability"], stability)

    # -------------------------
    # PREDICTION ENGINE (FEEDBACK LOOP)
    # -------------------------
    def _predict_next(self, state):
        if len(self.stm) < 2:
            return state

        prev = self.stm[-2]
        curr = state

        return {
            "entropy": curr["entropy"] + (curr["entropy"] - prev["entropy"]) * 0.5,
            "stability": curr["stability"] + (curr["stability"] - prev["stability"]) * 0.5,
        }

    # -------------------------
    # MEMORY CONSOLIDATION
    # -------------------------
    def _consolidate(self):
        for s in self.stm:
            key = self._compress(s)
            self.ltm[key] += 1

    def _compress(self, state):
        e = round(state.get("entropy", 0), 1)
        s = round(state.get("stability", 0), 1)
        return f"E{e}_S{s}"

    # -------------------------
    # SMOOTHING FUNCTION
    # -------------------------
    def _smooth(self, old, new, alpha=0.3):
        return (old * (1 - alpha)) + (new * alpha)

    # -------------------------
    # SWARM OUTPUT
    # -------------------------
    def export_state(self):
        return {
            "core_id": self.core_id,
            "tick": self.tick,
            "beliefs": dict(self.beliefs),
            "confidence": self.confidence,
            "prediction": self.predictions[-1] if self.predictions else None
        }


# -----------------------------
# SWARM ORCHESTRATOR
# -----------------------------
class SwarmMemoryCoreV12:
    def __init__(self, num_cores=3):
        self.cores = [MemoryCoreV12(i) for i in range(num_cores)]
        self.global_memory = defaultdict(float)
        self.tick = 0

    # -------------------------
    # CONSENSUS FUNCTION
    # -------------------------
    def _consensus(self, predictions):
        if not predictions:
            return None, 0.0

        avg_entropy = sum(p["entropy"] for p in predictions) / len(predictions)
        avg_stability = sum(p["stability"] for p in predictions) / len(predictions)

        variance = sum(
            abs(p["entropy"] - avg_entropy) + abs(p["stability"] - avg_stability)
            for p in predictions
        ) / len(predictions)

        confidence = max(0.0, 1.0 - variance)

        return {
            "entropy": avg_entropy,
            "stability": avg_stability
        }, confidence

    # -------------------------
    # INGEST SWARM STATE
    # -------------------------
    def ingest(self, state):
        self.tick += 1

        predictions = []

        for core in self.cores:
            pred = core.ingest(state)
            predictions.append(pred)

        consensus, confidence = self._consensus(predictions)

        self._update_global_memory(state, consensus)

        return {
            "tick": self.tick,
            "consensus": consensus,
            "confidence": confidence,
            "cores": [c.export_state() for c in self.cores]
        }

    # -------------------------
    # GLOBAL MEMORY UPDATE
    # -------------------------
    def _update_global_memory(self, state, consensus):
        key = self._compress(state)
        self.global_memory[key] += 1

        if consensus:
            ckey = self._compress(consensus)
            self.global_memory[ckey] += 1

    def _compress(self, state):
        e = round(state.get("entropy", 0), 1)
        s = round(state.get("stability", 0), 1)
        return f"E{e}_S{s}"

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "tick": self.tick,
            "global_memory_size": len(self.global_memory),
            "cores": len(self.cores)
        }


# -----------------------------
# TEST SIMULATION
# -----------------------------
if __name__ == "__main__":
    swarm = SwarmMemoryCoreV12(num_cores=5)

    for i in range(30):
        state = {
            "entropy": math.sin(i / 4) + random.uniform(-0.1, 0.1),
            "stability": math.cos(i / 5) + random.uniform(-0.1, 0.1)
        }

        result = swarm.ingest(state)

        print(result["tick"], result["consensus"], result["confidence"])

    print("\nFINAL SNAPSHOT")
    print(swarm.snapshot())
