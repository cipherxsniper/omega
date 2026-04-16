import json
import time
import os
import hashlib
from collections import defaultdict, Counter

# =========================================================
# STORAGE
# =========================================================

MEMORY_FILE = "runtime_v7/supervisor/cognitive_memory_graph.json"
PRED_FILE   = "runtime_v7/supervisor/prediction_mesh_v12.json"
TRUST_FILE  = "runtime_v7/supervisor/trust_db_v12.json"

os.makedirs("runtime_v7/supervisor", exist_ok=True)


# =========================================================
# UTIL
# =========================================================

def load_json(path, default):
    if os.path.exists(path):
        return json.load(open(path))
    return default


def save_json(path, data):
    json.dump(data, open(path, "w"), indent=2)


def sign(node_id, data):
    raw = json.dumps(data, sort_keys=True).encode()
    return hashlib.sha256(node_id.encode() + raw).hexdigest()


def verify(node_id, data, signature):
    return sign(node_id, data) == signature


# =========================================================
# 🧠 V12 CAUSAL ENGINE
# =========================================================

class CausalEngineV12:

    def __init__(self):
        self.causal_map = defaultdict(Counter)

    def build_causal_graph(self, events):
        for i in range(len(events) - 1):
            a = events[i]
            b = events[i + 1]

            cause = a.get("type")
            effect = b.get("type")

            if cause and effect:
                self.causal_map[cause][effect] += 1

    def causal_inference(self, cause):
        effects = self.causal_map.get(cause, None)

        if not effects:
            return {"effect": None, "confidence": 0.0}

        total = sum(effects.values())
        best = effects.most_common(1)[0]

        return {
            "cause": cause,
            "effect": best[0],
            "confidence": round(best[1] / total, 3)
        }


# =========================================================
# 🌐 V12 DISTRIBUTED MESH
# =========================================================

class PredictionMeshV12:

    def __init__(self):
        self.local_predictions = []

    def add_prediction(self, node_id, prediction, confidence):
        self.local_predictions.append({
            "node": node_id,
            "prediction": prediction,
            "confidence": confidence
        })

    def aggregate(self):
        if not self.local_predictions:
            return {}

        scores = defaultdict(float)
        weights = defaultdict(float)

        for p in self.local_predictions:
            node = p["node"]
            pred = p["prediction"]
            conf = p["confidence"]

            scores[pred] += conf
            weights[pred] += 1

        best = max(scores.items(), key=lambda x: x[1])

        return {
            "consensus_prediction": best[0],
            "confidence": round(best[1] / max(1, sum(weights.values())), 3),
            "contributors": len(self.local_predictions)
        }


# =========================================================
# 🔐 V12 SECURITY LAYER
# =========================================================

class SecurityLayerV12:

    def __init__(self):
        self.trust_db = load_json(TRUST_FILE, {})

    def trust(self, node_id):
        return self.trust_db.get(node_id, 0.5)

    def validate_prediction(self, node_id, prediction):
        # reject low trust nodes
        if self.trust(node_id) < 0.2:
            return False

        # reject malformed predictions
        if not prediction:
            return False

        return True

    def update_trust(self, node_id, delta):
        self.trust_db[node_id] = max(0.0, min(1.0, self.trust(node_id) + delta))
        save_json(TRUST_FILE, self.trust_db)


# =========================================================
# 🧠 V12 ORCHESTRATOR
# =========================================================

class V12SwarmIntelligence:

    def __init__(self):
        self.causal = CausalEngineV12()
        self.mesh = PredictionMeshV12()
        self.security = SecurityLayerV12()

    def step(self):

        memory = load_json(MEMORY_FILE, {"events": []})
        events = memory.get("events", [])

        # -------------------------
        # CAUSAL BUILD
        # -------------------------
        self.causal.build_causal_graph(events)

        if len(events) < 2:
            return

        last = events[-1]
        node = last.get("node", "unknown")
        event_type = last.get("type")

        # -------------------------
        # CAUSAL INFERENCE
        # -------------------------
        inference = self.causal.causal_inference(event_type)

        # -------------------------
        # SECURITY CHECK
        # -------------------------
        if not self.security.validate_prediction(node, inference):
            self.security.update_trust(node, -0.1)
            return

        # -------------------------
        # MESH SHARE
        # -------------------------
        self.mesh.add_prediction(
            node,
            inference["effect"],
            inference["confidence"]
        )

        consensus = self.mesh.aggregate()

        # -------------------------
        # OUTPUT
        # -------------------------
        result = {
            "causal_inference": inference,
            "mesh": consensus,
            "active_nodes": len(self.mesh.local_predictions)
        }

        save_json(PRED_FILE, result)

        print("[V12 INTELLIGENCE]")
        print(json.dumps(result, indent=2))


# =========================================================
# RUN LOOP
# =========================================================

def run():
    engine = V12SwarmIntelligence()

    while True:
        engine.step()
        time.sleep(5)


if __name__ == "__main__":
    print("🧠🌐🔐 V12 SWARM INTELLIGENCE MESH ONLINE")
    run()
