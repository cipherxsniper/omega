import time
import json
import random
import threading
from collections import defaultdict, deque

# =========================
# OMEGA MESH KERNEL V2
# Swarm Networking Layer
# =========================

class OmegaNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.memory = deque(maxlen=100)
        self.state = {
            "energy": random.random(),
            "coherence": random.random(),
            "last_beat": time.time()
        }

    def update(self, data):
        self.memory.append(data)
        self.state["coherence"] = min(1.0, self.state["coherence"] + 0.01)

class OmegaSwarmBus:
    def __init__(self):
        self.nodes = {}
        self.messages = deque(maxlen=500)
        self.global_state = {
            "tick": 0,
            "entropy": 0.5,
            "consensus": 1.0
        }

    # -------------------------
    # NODE MANAGEMENT
    # -------------------------
    def register_node(self, node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = OmegaNode(node_id)
            print(f"[OMEGA] Node registered: {node_id}")

    # -------------------------
    # MESSAGE PASSING
    # -------------------------
    def send_message(self, sender, receiver, payload):
        msg = {
            "from": sender,
            "to": receiver,
            "payload": payload,
            "timestamp": time.time()
        }
        self.messages.append(msg)

        if receiver in self.nodes:
            self.nodes[receiver].update(msg)

    # -------------------------
    # SWARM SYNCHRONIZATION
    # -------------------------
    def heartbeat(self):
        while True:
            self.global_state["tick"] += 1

            # entropy drift simulation
            self.global_state["entropy"] += random.uniform(-0.01, 0.01)
            self.global_state["entropy"] = max(0, min(1, self.global_state["entropy"]))

            # consensus stabilizes with node count
            n = len(self.nodes) + 1
            self.global_state["consensus"] = 1 - (self.global_state["entropy"] / n)

            for node in self.nodes.values():
                node.state["last_beat"] = time.time()

            time.sleep(1)

    # -------------------------
    # OMEGA TIME COMMAND
    # -------------------------
    def omega_time(self):
        return {
            "unix": time.time(),
            "tick": self.global_state["tick"],
            "entropy": round(self.global_state["entropy"], 4),
            "consensus": round(self.global_state["consensus"], 4),
            "nodes": len(self.nodes)
        }

    # -------------------------
    # BROADCAST THINKING
    # -------------------------
    def broadcast(self, payload):
        for node_id in self.nodes:
            self.send_message("OMEGA_CORE", node_id, payload)

# =========================
# DEMO EXECUTION
# =========================
if __name__ == "__main__":
    swarm = OmegaSwarmBus()

    swarm.register_node("node_alpha")
    swarm.register_node("node_beta")
    swarm.register_node("node_gamma")

    # start heartbeat thread
    t = threading.Thread(target=swarm.heartbeat, daemon=True)
    t.start()

    # simulate swarm activity
    for i in range(20):
        swarm.broadcast({"thought": f"emergent_signal_{i}", "strength": random.random()})
        print("[OMEGA TIME]", swarm.omega_time())
        time.sleep(1)

    print("\nFINAL STATE:")
    print(json.dumps(swarm.omega_time(), indent=2))
