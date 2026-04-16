import time
import random
import threading
from collections import deque

# =========================
# OMEGA MESH KERNEL V7
# Self-Aware Cognition Kernel
# =========================

# -------------------------
# SELF MODEL (META LAYER)
# -------------------------
class SelfModel:
    def __init__(self):
        self.history = deque(maxlen=200)
        self.predictions = deque(maxlen=200)
        self.confidence = 1.0

    # predict next internal state
    def predict(self, state):
        guess = {
            "expected_coherence": state.get("coherence", 0.5) + random.uniform(-0.05, 0.05),
            "expected_stability": state.get("stability", 0.5) + random.uniform(-0.05, 0.05),
        }
        self.predictions.append(guess)
        return guess

    # compare prediction vs reality
    def update_confidence(self, actual):
        if not self.predictions:
            return

        pred = self.predictions[-1]

        error = abs(pred["expected_coherence"] - actual["coherence"]) + \
                abs(pred["expected_stability"] - actual["stability"])

        self.confidence *= (1 - min(0.1, error))

        self.history.append({
            "pred": pred,
            "actual": actual,
            "error": error
        })


# -------------------------
# NODE WITH SELF-AWARENESS
# -------------------------
class OmegaNode:
    def __init__(self, node_id):
        self.id = node_id

        self.state = {
            "coherence": 0.5,
            "stability": 0.5,
            "awareness": 0.2
        }

        self.self_model = SelfModel()

    # -------------------------
    # THINK
    # -------------------------
    def think(self):
        prediction = self.self_model.predict(self.state)

        # simulate cognition drift
        self.state["coherence"] += random.uniform(-0.03, 0.03)
        self.state["stability"] += random.uniform(-0.02, 0.02)

        # awareness grows from stability + coherence alignment
        alignment = 1 - abs(
            self.state["coherence"] - self.state["stability"]
        )

        self.state["awareness"] = max(0, min(1, alignment))

        self.self_model.update_confidence(self.state)

        return prediction


# -------------------------
# SELF-AWARE SWARM BRAIN
# -------------------------
class OmegaSwarmBus:
    def __init__(self):
        self.nodes = {}

        self.global_state = {
            "tick": 0,
            "self_awareness": 0.0,
            "system_confidence": 1.0
        }

    # -------------------------
    # REGISTER NODE
    # -------------------------
    def register(self, node_id):
        self.nodes[node_id] = OmegaNode(node_id)
        print(f"[OMEGA V7] Node self-model active: {node_id}")

    # -------------------------
    # SYSTEM SELF REFLECTION
    # -------------------------
    def reflect(self):
        avg_awareness = sum(
            n.state["awareness"] for n in self.nodes.values()
        ) / len(self.nodes)

        avg_conf = sum(
            n.self_model.confidence for n in self.nodes.values()
        ) / len(self.nodes)

        self.global_state["self_awareness"] = avg_awareness
        self.global_state["system_confidence"] = avg_conf

    # -------------------------
    # COGNITION LOOP
    # -------------------------
    def heartbeat(self):
        while True:
            self.global_state["tick"] += 1

            for node in self.nodes.values():
                node.think()

            self.reflect()

            time.sleep(1)

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "tick": self.global_state["tick"],
            "self_awareness": round(self.global_state["self_awareness"], 4),
            "system_confidence": round(self.global_state["system_confidence"], 4),
            "nodes": len(self.nodes)
        }


# =========================
# DEMO
# =========================
if __name__ == "__main__":
    swarm = OmegaSwarmBus()

    swarm.register("A")
    swarm.register("B")
    swarm.register("C")
    swarm.register("D")

    threading.Thread(target=swarm.heartbeat, daemon=True).start()

    while True:
        time.sleep(2)
        print("[OMEGA V7]", swarm.snapshot())
