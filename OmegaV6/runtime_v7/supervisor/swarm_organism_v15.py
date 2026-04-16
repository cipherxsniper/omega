import json
import time
import random
import os
from collections import defaultdict, Counter

# =========================================================
# STORAGE
# =========================================================

MEMORY_FILE = "runtime_v7/supervisor/global_memory_v15.json"
DRIFT_FILE  = "runtime_v7/supervisor/drift_report_v15.json"
CLUSTER_FILE = "runtime_v7/supervisor/cluster_federation_v15.json"

os.makedirs("runtime_v7/supervisor", exist_ok=True)


# =========================================================
# 🧠 EMERGENT INTELLIGENCE ENGINE
# =========================================================

class EmergentGraphV15:

    def __init__(self):
        self.patterns = defaultdict(Counter)
        self.global_signals = Counter()

    def ingest(self, event):
        etype = event.get("type")
        node = event.get("node_id")

        self.patterns[node][etype] += 1
        self.global_signals[etype] += 1

    def detect_emergence(self):

        total = sum(self.global_signals.values()) or 1

        signals = {
            k: round(v / total, 3)
            for k, v in self.global_signals.items()
        }

        dominant = max(self.global_signals.items(), key=lambda x: x[1])

        return {
            "global_distribution": signals,
            "dominant_behavior": dominant[0],
            "strength": round(dominant[1] / total, 3)
        }


# =========================================================
# 🔧 SELF-REPAIR ENGINE
# =========================================================

class SelfRepairV15:

    def __init__(self):
        self.drift_history = []

    def detect_drift(self, memory_before, memory_after):

        drift_score = abs(len(memory_before) - len(memory_after)) / max(1, len(memory_before))

        return drift_score

    def repair(self, drift_score):

        if drift_score > 0.3:
            action = "REBALANCE_MEMORY_GRAPH"
        elif drift_score > 0.1:
            action = "ADJUST_ROUTING_WEIGHTS"
        else:
            action = "STABLE"

        self.drift_history.append({
            "drift": drift_score,
            "action": action,
            "time": time.time()
        })

        return action


# =========================================================
# 🌍 MULTI-WAN FEDERATION LAYER
# =========================================================

class WANFederationV15:

    def __init__(self):
        self.regions = {
            "NA": {"nodes": 3, "health": 0.9},
            "EU": {"nodes": 2, "health": 0.8},
            "ASIA": {"nodes": 4, "health": 0.85}
        }

    def sync(self):

        total_nodes = sum(r["nodes"] for r in self.regions.values())

        global_health = sum(
            r["health"] * r["nodes"] for r in self.regions.values()
        ) / total_nodes

        return {
            "total_nodes": total_nodes,
            "global_health": round(global_health, 3),
            "regions": self.regions
        }


# =========================================================
# 🧬 SWARM ORCHESTRATOR
# =========================================================

class SwarmV15:

    def __init__(self):
        self.memory = defaultdict(list)
        self.emergent = EmergentGraphV15()
        self.repair = SelfRepairV15()
        self.federation = WANFederationV15()

    # -------------------------
    # PROCESS EVENT
    # -------------------------
    def process(self, event):

        before = dict(self.memory)

        node = event["node_id"]
        self.memory[node].append(event)

        self.emergent.ingest(event)

        after = dict(self.memory)

        drift = self.repair.detect_drift(before, after)
        action = self.repair.repair(drift)

        print("\n[V15 EVENT]")
        print(json.dumps(event, indent=2))

        print(f"[V15 DRIFT] {drift:.3f}")
        print(f"[V15 REPAIR ACTION] {action}")

    # -------------------------
    # ANALYZE EMERGENCE
    # -------------------------
    def analyze(self):

        return self.emergent.detect_emergence()

    # -------------------------
    # FEDERATION STATUS
    # -------------------------
    def federation_status(self):

        return self.federation.sync()

    # -------------------------
    # RUN LOOP
    # -------------------------
    def run(self):

        while True:

            event = {
                "node_id": f"node-{random.randint(1,5)}",
                "type": random.choice([
                    "heartbeat",
                    "ack",
                    "sync",
                    "error",
                    "query"
                ]),
                "timestamp": time.time()
            }

            self.process(event)

            # emergent intelligence snapshot
            if random.random() > 0.6:
                print("\n[🧠 V15 EMERGENT STATE]")
                print(json.dumps(self.analyze(), indent=2))

            # WAN federation snapshot
            if random.random() > 0.7:
                print("\n[🌍 V15 FEDERATION STATUS]")
                print(json.dumps(self.federation_status(), indent=2))

            time.sleep(2)


# =========================================================
# BOOT
# =========================================================

if __name__ == "__main__":
    print("🧬🌐🧠 V15 SWARM ORGANISM ONLINE — SELF-HEALING + EMERGENT + FEDERATED")
    SwarmV15().run()
