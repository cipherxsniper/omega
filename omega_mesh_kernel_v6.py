import time
import random
import threading
from collections import defaultdict, deque

# =========================
# OMEGA MESH KERNEL V6
# Consciousness Stabilization Layer
# =========================

# -------------------------
# PERSISTENT MEMORY STORE
# -------------------------
class MemoryStore:
    def __init__(self):
        self.short_term = deque(maxlen=300)
        self.long_term = defaultdict(float)

    def write_stm(self, item):
        self.short_term.append(item)

    def consolidate(self):
        for item in self.short_term:
            key = item.get("signature", "unknown")
            self.long_term[key] += item.get("strength", 0.1)

        # decay noise
        for k in list(self.long_term.keys()):
            self.long_term[k] *= 0.99
            if self.long_term[k] < 0.05:
                del self.long_term[k]


# -------------------------
# NODE WITH IDENTITY STABILITY
# -------------------------
class OmegaNode:
    def __init__(self, node_id):
        self.id = node_id

        self.memory = MemoryStore()

        self.identity = {
            "coherence": 0.5,
            "stability": 0.5,
            "reputation": 1.0
        }

        self.goal_vector = random.random()

    # -------------------------
    # STABLE LEARNING
    # -------------------------
    def perceive(self, idea):
        signature = idea.content[:10]

        self.memory.write_stm({
            "signature": signature,
            "strength": idea.strength
        })

        self.identity["coherence"] += 0.01 * idea.strength
        self.identity["stability"] += 0.005

    # -------------------------
    # NODE THINKING
    # -------------------------
    def think(self):
        drift = abs(self.goal_vector - self.identity["coherence"])

        return {
            "content": f"thought_{self.id}_{random.randint(1,999)}",
            "strength": max(0, 1 - drift),
            "signature": self.id
        }

    # -------------------------
    # UPDATE STABILITY
    # -------------------------
    def stabilize(self):
        self.memory.consolidate()

        # clamp identity
        for k in self.identity:
            self.identity[k] = max(0, min(1.0, self.identity[k]))

        # reputation emerges from memory density
        self.identity["reputation"] = min(
            2.0,
            len(self.memory.long_term) / 50 + self.identity["stability"]
        )


# -------------------------
# CONSCIOUSNESS FIELD
# -------------------------
class OmegaSwarmBus:
    def __init__(self):
        self.nodes = {}

        self.state = {
            "tick": 0,
            "entropy": 0.5,
            "stability": 1.0,
            "coherence": 0.5
        }

    # -------------------------
    # REGISTER NODE
    # -------------------------
    def register(self, node_id):
        self.nodes[node_id] = OmegaNode(node_id)
        print(f"[OMEGA V6] Node stabilized: {node_id}")

    # -------------------------
    # BROADCAST EXPERIENCE
    # -------------------------
    def broadcast(self, idea):
        for node in self.nodes.values():
            node.perceive(idea)

    # -------------------------
    # GLOBAL STABILITY ENGINE
    # -------------------------
    def heartbeat(self):
        while True:
            self.state["tick"] += 1

            new_thoughts = []

            # NODE THINKING
            for node in self.nodes.values():
                node.stabilize()

                thought = node.think()
                new_thoughts.append(thought)

            # BROADCAST LOOP
            for t in new_thoughts:
                self.broadcast(t)

            # SYSTEM METRICS

            avg_coh = sum(n.identity["coherence"] for n in self.nodes.values()) / len(self.nodes)
            avg_stb = sum(n.identity["stability"] for n in self.nodes.values()) / len(self.nodes)
            avg_rep = sum(n.identity["reputation"] for n in self.nodes.values()) / len(self.nodes)

            self.state["coherence"] = avg_coh
            self.state["stability"] = avg_stb

            # entropy = instability inverse
            self.state["entropy"] = max(0, 1 - avg_stb)

            time.sleep(1)

    # -------------------------
    # SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "tick": self.state["tick"],
            "entropy": round(self.state["entropy"], 4),
            "stability": round(self.state["stability"], 4),
            "coherence": round(self.state["coherence"], 4),
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

    threading.Thread(target=swarm.heartbeat, daemon=True).start()

    while True:
        time.sleep(2)
        print("[OMEGA V6]", swarm.snapshot())
