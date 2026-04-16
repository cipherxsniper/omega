import socket
import threading
import json
import time
import hashlib


# ==============================
# V8.7 + V8.8 SWARM CORE SYSTEM
# ==============================

class OmegaSwarmV88:
    def __init__(self, port=6008):
        self.port = port
        self.running = True

        self.peers = {}
        self.trust = {}
        self.latency = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        print("[V8.8] SWARM CORE ONLINE on port", self.port, flush=True)

    # --------------------------
    # IDENTITY ENGINE (V8.8)
    # --------------------------
    def verify_node(self, node_id):
        # simple anti-fake-node layer
        if not node_id:
            return False

        if len(node_id) < 8:
            return False

        return True

    # --------------------------
    # PEER REGISTRY
    # --------------------------
    def register_peer(self, node_id):
        if not self.verify_node(node_id):
            return

        if node_id not in self.peers:
            self.peers[node_id] = time.time()
            self.trust[node_id] = 1.0
            self.latency[node_id] = 50

        else:
            self.peers[node_id] = time.time()
            self.trust[node_id] = min(1.0, self.trust[node_id] + 0.01)

    # --------------------------
    # SCORING ENGINE (V8.7)
    # --------------------------
    def score(self, node_id):
        trust = self.trust.get(node_id, 0.5)
        latency = self.latency.get(node_id, 100)

        return trust * (100 / (latency + 1))

    def best_peer(self):
        if not self.peers:
            return None

        return max(self.peers.keys(), key=self.score)

    # --------------------------
    # ROUTING ENGINE
    # --------------------------
    def route(self, payload):
        target = self.best_peer()

        if not target:
            return {"status": "no_peers"}

        return {
            "status": "routed",
            "target": target,
            "score": self.score(target),
            "payload": payload
        }

    # --------------------------
    # RX ENGINE
    # --------------------------
    def listen(self):
        print("[V8.8] RX ENGINE STARTED", flush=True)

        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                node_id = payload.get("node_id")

                if self.verify_node(node_id):
                    self.register_peer(node_id)

                print("[V8.8 RX]", payload, flush=True)

                # log persistence
                with open("logs/swarm_v88_rx.log", "a") as f:
                    f.write(json.dumps(payload) + "\n")

            except Exception as e:
                print("[RX ERROR]", e, flush=True)

    # --------------------------
    # HEARTBEAT ENGINE
    # --------------------------
    def heartbeat(self):
        while self.running:
            try:
                msg = {
                    "node_id": "local_node_v88",
                    "type": "heartbeat",
                    "timestamp": time.time()
                }

                data = json.dumps(msg).encode()
                self.sock.sendto(data, ("127.0.0.1", self.port))

                print("[V8.8 TX] heartbeat sent", flush=True)

            except Exception as e:
                print("[TX ERROR]", e, flush=True)

            time.sleep(3)

    # --------------------------
    # START SYSTEM
    # --------------------------
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        print("[V8.8] SYSTEM RUNNING", flush=True)

        while True:
            time.sleep(5)


if __name__ == "__main__":
    OmegaSwarmV88().start()
