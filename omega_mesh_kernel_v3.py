import time
import random
import threading
from collections import defaultdict, deque

# =========================
# OMEGA MESH KERNEL V3
# Swarm Cognition Upgrade
# =========================

class OmegaNode:
    def __init__(self, node_id):
        self.id = node_id
        self.memory = deque(maxlen=200)
        self.patterns = defaultdict(int)

        self.reputation = 1.0
        self.coherence = 0.5
        self.last_active = time.time()

    # -------------------------
    # LEARNING FROM MESSAGE
    # -------------------------
    def learn(self, msg):
        self.memory.append(msg)

        key = self._compress(msg)
        self.patterns[key] += 1

        # adjust internal coherence
        self.coherence += 0.01 * (1 if msg.get("strength", 0) > 0.5 else -0.005)
        self.coherence = max(0, min(1, self.coherence))

    # -------------------------
    # SIMPLE PATTERN COMPRESSION
    # -------------------------
    def _compress(self, msg):
        t = msg.get("type", "x")
        s = round(msg.get("strength", 0), 1)
        return f"{t}_{s}"

    # -------------------------
    # REPUTATION UPDATE
    # -------------------------
    def update_reputation(self):
        diversity = len(self.patterns)
        self.reputation = min(2.0, 0.5 + (diversity / 50) + self.coherence)


class OmegaSwarmBus:
    def __init__(self):
        self.nodes = {}
        self.messages = deque(maxlen=1000)

        self.global_state = {
            "tick": 0,
            "entropy": 0.5,
            "consensus": 1.0,
            "thought_chain": []
        }

    # -------------------------
    # NODE MANAGEMENT
    # -------------------------
    def register_node(self, node_id):
        self.nodes[node_id] = OmegaNode(node_id)
        print(f"[OMEGA] Node online: {node_id}")

    # -------------------------
    # MESSAGE ROUTING
    # -------------------------
    def send(self, sender, receiver, payload):
        msg = {
            "from": sender,
            "to": receiver,
            "type": payload.get("type", "thought"),
            "strength": payload.get("strength", random.random()),
            "timestamp": time.time()
        }

        self.messages.append(msg)

        if receiver in self.nodes:
            self.nodes[receiver].learn(msg)

        # feed into global cognition
        self._update_thought_chain(msg)

    # -------------------------
    # EMERGENT THOUGHT CHAIN
    # -------------------------
    def _update_thought_chain(self, msg):
        chain = self.global_state["thought_chain"]

        if len(chain) > 50:
            chain.pop(0)

        chain.append(msg)

        # compress into entropy signal
        self.global_state["entropy"] += (0.001 if msg["strength"] > 0.5 else -0.001)
        self.global_state["entropy"] = max(0, min(1, self.global_state["entropy"]))

    # -------------------------
    # SWARM CONSENSUS ENGINE
    # -------------------------
    def _compute_consensus(self):
        if not self.nodes:
            return 1.0

        rep_sum = sum(n.reputation for n in self.nodes.values())
        coh_sum = sum(n.coherence for n in self.nodes.values())

        n = len(self.nodes)
        return (rep_sum / n) * (coh_sum / n)

    # -------------------------
    # SWARM LOOP
    # -------------------------
    def heartbeat(self):
        while True:
            self.global_state["tick"] += 1

            # update node reputations
            for node in self.nodes.values():
                node.update_reputation()
                node.last_active = time.time()

            # recompute consensus
            self.global_state["consensus"] = self._compute_consensus()

            time.sleep(1)

    # -------------------------
    # BROADCAST THINKING
    # -------------------------
    def broadcast(self, payload):
        for node_id in self.nodes:
            self.send("OMEGA_CORE", node_id, payload)

    # -------------------------
    # SYSTEM SNAPSHOT
    # -------------------------
    def snapshot(self):
        return {
            "tick": self.global_state["tick"],
            "entropy": round(self.global_state["entropy"], 4),
            "consensus": round(self.global_state["consensus"], 4),
            "nodes": len(self.nodes),
            "thought_chain_len": len(self.global_state["thought_chain"])
        }


# =========================
# DEMO RUN
# =========================
if __name__ == "__main__":
    swarm = OmegaSwarmBus()

    swarm.register_node("alpha")
    swarm.register_node("beta")
    swarm.register_node("gamma")
    swarm.register_node("delta")

    threading.Thread(target=swarm.heartbeat, daemon=True).start()

    for i in range(30):
        swarm.broadcast({
            "type": "idea",
            "strength": random.random()
        })

        print("[OMEGA SNAPSHOT]", swarm.snapshot())
        time.sleep(1)
