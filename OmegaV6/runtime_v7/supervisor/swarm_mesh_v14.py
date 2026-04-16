import json
import time
import os
import uuid
import hashlib
import random
from collections import defaultdict

# =========================================================
# STORAGE
# =========================================================

MEMORY_FILE = "runtime_v7/supervisor/global_memory_v14.json"
NODE_FILE   = "runtime_v7/supervisor/node_registry_v14.json"

os.makedirs("runtime_v7/supervisor", exist_ok=True)


# =========================================================
# 🔐 CRYPTO IDENTITY LAYER
# =========================================================

class CryptoIdentityV14:

    def __init__(self):
        self.node_id = str(uuid.uuid4())
        self.private_key = self._generate_key()
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

    def _generate_key(self):
        return str(uuid.uuid4()) + str(time.time())

    def sign(self, payload: dict):
        raw = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(raw + self.private_key.encode()).hexdigest()

    def verify(self, payload: dict, signature: str, public_key: str):
        # simplified verification model
        expected = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode() + self.private_key.encode()
        ).hexdigest()

        return signature == expected


# =========================================================
# 🌐 MESH ROUTER
# =========================================================

class MeshRouterV14:

    def __init__(self):
        self.nodes = {}

    def register_node(self, node_id, trust=0.5, latency=1.0, uptime=1.0):
        self.nodes[node_id] = {
            "trust": trust,
            "latency": latency,
            "uptime": uptime
        }

    def route(self, event):
        if not self.nodes:
            return None

        def score(n):
            d = self.nodes[n]
            return d["trust"] * d["uptime"] / max(0.1, d["latency"])

        best = max(self.nodes.keys(), key=score)
        return best


# =========================================================
# 🧠 GLOBAL CONSENSUS MEMORY
# =========================================================

class GlobalMemoryV14:

    def __init__(self):
        self.memory = defaultdict(lambda: defaultdict(int))

    def ingest(self, event):
        etype = event.get("type")
        node = event.get("node_id", "unknown")

        self.memory[node][etype] += 1

    def consensus(self):
        result = {}

        for node, events in self.memory.items():
            total = sum(events.values())
            result[node] = {
                k: round(v / total, 3)
                for k, v in events.items()
            }

        return result


# =========================================================
# 🧬 SWARM ORCHESTRATOR
# =========================================================

class SwarmV14:

    def __init__(self):
        self.crypto = CryptoIdentityV14()
        self.router = MeshRouterV14()
        self.memory = GlobalMemoryV14()

        # bootstrap fake nodes for routing simulation
        self.router.register_node("node-A", trust=0.8, latency=0.3)
        self.router.register_node("node-B", trust=0.6, latency=0.6)
        self.router.register_node("node-C", trust=0.9, latency=0.2)

    # -------------------------
    # PROCESS EVENT
    # -------------------------
    def process(self, event):

        # sign event
        signature = self.crypto.sign(event)

        # verify event (self-check simulation)
        if not self.crypto.verify(event, signature, self.crypto.public_key):
            print("[V14 SECURITY] invalid signature rejected")
            return

        # ingest into memory graph
        self.memory.ingest(event)

        # route decision
        target = self.router.route(event)

        print("\n[V14 EVENT]")
        print(json.dumps(event, indent=2))
        print(f"[V14 ROUTED TO] {target}")

    # -------------------------
    # SIM LOOP
    # -------------------------
    def run(self):

        while True:

            event = {
                "node_id": f"node-{random.randint(1,3)}",
                "type": random.choice(["heartbeat", "ack", "error", "sync"]),
                "timestamp": time.time()
            }

            self.process(event)

            if random.random() > 0.7:
                print("\n[V14 MEMORY CONSENSUS]")
                print(json.dumps(self.memory.consensus(), indent=2))

            time.sleep(2)


# =========================================================
# BOOT
# =========================================================

if __name__ == "__main__":
    print("🌐🧠🔐 V14 SWARM MESH INTELLIGENCE ONLINE")
    SwarmV14().run()
