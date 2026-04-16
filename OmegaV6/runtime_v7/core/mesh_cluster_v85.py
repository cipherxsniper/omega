import socket
import threading
import json
import time
import hashlib


# -----------------------------
# 🔐 TRUST REGISTRY (V8.5 CORE)
# -----------------------------
class TrustRegistryV85:
    def __init__(self):
        self.trusted_nodes = set()

    def register(self, node_id: str):
        self.trusted_nodes.add(node_id)

    def is_trusted(self, node_id: str):
        if not node_id:
            return False
        return node_id in self.trusted_nodes


# -----------------------------
# 🧠 SECURE MESH CLUSTER V8.5
# -----------------------------
class MeshClusterV85:
    def __init__(self, port=6001):
        self.port = port
        self.peers = {}
        self.running = True

        self.registry = TrustRegistryV85()

        # UDP socket (Termux-safe)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        # self trust bootstrap (allow self node initially)
        self.node_id = self.generate_node_id()
        self.registry.register(self.node_id)

    # -----------------------------
    # 🧬 NODE IDENTITY
    # -----------------------------
    def generate_node_id(self):
        raw = f"{socket.gethostname()}:{time.time()}:{random_seed()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    # -----------------------------
    # 📡 BROADCAST LOOP (SAFE)
    # -----------------------------
    def broadcast(self):
        while self.running:
            try:
                payload = {
                    "node_id": self.node_id,
                    "timestamp": time.time(),
                    "type": "omega_v8_5_cluster_node"
                }

                data = json.dumps(payload).encode()

                # loopback mesh (Termux-safe)
                targets = ["127.0.0.1"]

                for ip in targets:
                    self.sock.sendto(data, (ip, self.port))

                # self-register heartbeat
                self.registry.register(self.node_id)

            except Exception as e:
                print("[BROADCAST ERROR]", e)

            time.sleep(2)

    # -----------------------------
    # 📥 LISTEN LOOP (SECURITY LAYER)
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                # 🔐 reject fake nodes
                if not self.registry.is_trusted(payload.get("node_id")):
                    return

                node_id = payload.get("node_id")

                self.peers[node_id] = time.time()

                print("[SECURE RX]", payload)

            except Exception:
                pass

    # -----------------------------
    # 🚀 START CLUSTER
    # -----------------------------
    def start(self):
        print("[V8.5] SECURE SWARM MESH ONLINE")

        t1 = threading.Thread(target=self.broadcast, daemon=True)
        t2 = threading.Thread(target=self.listen, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(5)
            print({
                "node": self.node_id[:12],
                "peers": len(self.peers)
            })


# -----------------------------
# 🧪 SAFE SEED GENERATOR
# -----------------------------
def random_seed():
    return str(time.time_ns())


# -----------------------------
# ▶️ RUN
# -----------------------------
if __name__ == "__main__":
    MeshClusterV85().start()
