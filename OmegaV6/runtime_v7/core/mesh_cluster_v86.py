import socket
import threading
import json
import time
import hashlib

from runtime_v7.core.v86_peer_enrollment import PeerEnrollmentV86
from runtime_v7.core.v86_trust_registry import TrustRegistryV86
from runtime_v7.core.v86_lan_discovery import LANDiscoveryV86


class MeshClusterV86:
    def __init__(self, port=6001):
        self.port = port

        self.peers = {}
        self.running = True

        # 🔐 trust + enrollment systems
        self.registry = TrustRegistryV86()
        self.enroller = PeerEnrollmentV86(identity=self, registry=self.registry)

        # 🌐 LAN discovery
        self.discovery = LANDiscoveryV86()

        # socket setup (Termux safe)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(("0.0.0.0", self.port))
        except OSError:
            print("[V8.6] Port in use, switching mode to listen-only")

    # -----------------------------
    # 🧠 NODE ID (simple identity)
    # -----------------------------
    @property
    def node_id(self):
        return hashlib.sha256(str(self.port).encode()).hexdigest()[:16]

    # -----------------------------
    # 📡 BROADCAST (SAFE LOOPBACK)
    # -----------------------------
    def broadcast(self):
        while self.running:
            try:
                payload = {
                    "node_id": self.node_id,
                    "timestamp": time.time(),
                    "type": "cluster_ping"
                }

                data = json.dumps(payload).encode()

                # safe local mesh mode (Termux compatible)
                targets = ["127.0.0.1"]

                for ip in targets:
                    self.sock.sendto(data, (ip, self.port))

            except Exception as e:
                print("[BROADCAST ERROR]", e)

            time.sleep(2)

    # -----------------------------
    # 📥 RECEIVE LOOP
    # -----------------------------
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                # 🔐 reject fake / untrusted nodes
                if not self.registry.is_trusted(payload.get("node_id")):
                    # allow enrollment packets only
                    if payload.get("type") != "enroll_request":
                        continue

                # 🤝 enrollment handler (IMPORTANT HOOK)
                if payload.get("type") == "enroll_request":
                    self.enroller.handle_enroll({
                        "payload": payload,
                        "sig": hashlib.sha256(str(payload).encode()).hexdigest()
                    })
                    continue

                node_id = payload.get("node_id")

                if node_id:
                    self.peers[node_id] = time.time()
                    self.registry.update_seen(node_id)

                print("[V8.6 RX]", payload)

            except Exception:
                pass

    # -----------------------------
    # 🌐 LAN DISCOVERY SCAN
    # -----------------------------
    def discover(self):
        while self.running:
            try:
                found = self.discovery.scan_local_network(self.port)

                for ip in found:
                    print("[V8.6 DISCOVERED]", ip)

            except Exception as e:
                print("[DISCOVERY ERROR]", e)

            time.sleep(15)

    # -----------------------------
    # 🚀 START CLUSTER
    # -----------------------------
    def start(self):
        print(f"[V8.6] Mesh Cluster ONLINE on port {self.port}")

        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.broadcast, daemon=True).start()
        threading.Thread(target=self.discover, daemon=True).start()

        while True:
            time.sleep(5)


# -----------------------------
# 🚀 ENTRYPOINT
# -----------------------------
if __name__ == "__main__":
    MeshClusterV86().start()
