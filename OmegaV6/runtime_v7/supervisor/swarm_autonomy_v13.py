import json
import time
import os
import socket
import uuid
from threading import Thread
from collections import defaultdict

# =========================================================
# STORAGE
# =========================================================

STATE_FILE = "runtime_v7/supervisor/swarm_state_v13.json"
NODE_FILE  = "runtime_v7/supervisor/node_identity_v13.json"

os.makedirs("runtime_v7/supervisor", exist_ok=True)


# =========================================================
# UTIL
# =========================================================

def load(path, default):
    if os.path.exists(path):
        return json.load(open(path))
    return default


def save(path, data):
    json.dump(data, open(path, "w"), indent=2)


# =========================================================
# 🧬 IDENTITY CONTINUITY LAYER
# =========================================================

class IdentityCoreV13:

    def __init__(self):
        self.identity = load(NODE_FILE, None)

        if not self.identity:
            self.identity = {
                "node_id": str(uuid.uuid4()),
                "trust": 0.5,
                "created": time.time(),
                "last_seen": time.time(),
                "failures": 0
            }
            save(NODE_FILE, self.identity)

    def update_seen(self):
        self.identity["last_seen"] = time.time()
        save(NODE_FILE, self.identity)

    def adjust_trust(self, delta):
        self.identity["trust"] = max(0.0, min(1.0, self.identity["trust"] + delta))
        save(NODE_FILE, self.identity)


# =========================================================
# 🌐 FEDERATION LAYER (WAN READY)
# =========================================================

class FederationBusV13:

    def __init__(self, port=7013):
        self.port = port
        self.peers = set()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(("0.0.0.0", self.port))
        except:
            print("[V13 FEDERATION] already running")

        print(f"[V13 FEDERATION] ONLINE | port={self.port}")

    def register_peer(self, ip):
        self.peers.add(ip)

    def broadcast(self, msg):
        raw = json.dumps(msg).encode()
        for ip in self.peers:
            try:
                self.sock.sendto(raw, (ip, self.port))
            except:
                pass


# =========================================================
# 🛠️ SELF-HEALING ENGINE
# =========================================================

class SelfHealingV13:

    def __init__(self, identity: IdentityCoreV13):
        self.identity = identity
        self.failure_log = []

    def report_failure(self, layer, error):
        self.failure_log.append({
            "layer": layer,
            "error": str(error),
            "time": time.time()
        })

        self.identity.adjust_trust(-0.05)

        print(f"[V13 HEAL] failure in {layer}: {error}")

    def heal(self):
        if len(self.failure_log) > 3:
            print("[V13 HEAL] initiating recovery protocol")

            # reset failure pressure
            self.failure_log = []

            # restore trust slightly
            self.identity.adjust_trust(+0.1)


# =========================================================
# 🧠 ORCHESTRATOR
# =========================================================

class SwarmV13:

    def __init__(self):
        self.identity = IdentityCoreV13()
        self.federation = FederationBusV13()
        self.healer = SelfHealingV13(self.identity)

        self.running = True

    # -------------------------
    # CORE LOOP
    # -------------------------
    def run(self):

        while self.running:
            try:
                self.identity.update_seen()

                state = {
                    "node": self.identity.identity["node_id"],
                    "trust": self.identity.identity["trust"],
                    "timestamp": time.time()
                }

                self.federation.broadcast(state)

                print("[V13 SWARM]")
                print(json.dumps(state, indent=2))

                self.healer.heal()

                time.sleep(5)

            except Exception as e:
                self.healer.report_failure("core_loop", e)
                time.sleep(2)


# =========================================================
# BOOT
# =========================================================

if __name__ == "__main__":
    print("🧬🌍🛠️ V13 SWARM AUTONOMY SYSTEM ONLINE")
    SwarmV13().run()
