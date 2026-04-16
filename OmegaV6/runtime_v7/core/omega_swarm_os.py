import socket
import json
import time
import threading
import hashlib
import hmac
import random
from collections import defaultdict


class OmegaSwarmOS:
    """
    Unified Swarm Operating System Kernel
    - Identity-secure mesh
    - LAN discovery
    - Cognitive shared memory
    - Routing + trust scoring
    """

    def __init__(self, port=6000, key=b"OMEGA_SWARM_KEY_V9"):
        self.port = port
        self.key = key

        # 🧠 Core State
        self.node_id = self._generate_node_id()
        self.peers = {}            # active nodes
        self.trust = defaultdict(lambda: 1.0)
        self.latency = defaultdict(lambda: 1.0)

        # 🧭 Cognitive Layer
        self.memory = {}
        self.system_health = 1.0

        # 🌐 LAN Discovery Cache
        self.discovery_cache = {}

        # socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        print(f"[OMEGA SWARM OS] ONLINE | node={self.node_id} | port={self.port}")

    # =========================================================
    # 🧠 NODE ID
    # =========================================================
    def _generate_node_id(self):
        raw = f"{time.time()}-{random.random()}".encode()
        return hashlib.sha256(raw).hexdigest()[:16]

    # =========================================================
    # 🔐 V9.2 SECURITY LAYER (HMAC VERIFY)
    # =========================================================
    def sign(self, payload: dict):
        raw = json.dumps(payload, sort_keys=True).encode()
        return hmac.new(self.key, raw, hashlib.sha256).hexdigest()

    def verify_signature(self, payload: dict):
        if "sig" not in payload:
            return False

        sig = payload["sig"]
        raw = dict(payload)
        raw.pop("sig", None)

        expected = self.sign(raw)
        return hmac.compare_digest(sig, expected)

    # =========================================================
    # 🤝 ENROLLMENT SYSTEM (V8.6 UPGRADED)
    # =========================================================
    def handle_enroll(self, payload, addr):
        node = payload.get("node_id")

        if not node:
            return

        self.peers[node] = {
            "addr": addr,
            "last_seen": time.time(),
            "status": "active"
        }

        self.trust[node] = 1.0

        print(f"[ENROLL] Node accepted: {node}")

    # =========================================================
    # 🌐 LAN DISCOVERY LAYER
    # =========================================================
    def broadcast_discovery(self):
        msg = {
            "node_id": self.node_id,
            "type": "lan_discovery",
            "timestamp": time.time()
        }
        msg["sig"] = self.sign(msg)

        for i in range(1, 255):
            target = f"192.168.0.{i}"
            try:
                self.sock.sendto(json.dumps(msg).encode(), (target, self.port))
            except:
                pass

    # =========================================================
    # 📡 SWARM ROUTING ENGINE (V8.7)
    # =========================================================
    def route_score(self, node):
        return self.trust[node] / (self.latency[node] + 0.01)

    def best_peer(self):
        if not self.peers:
            return None

        return max(self.peers.keys(), key=self.route_score)

    # =========================================================
    # 🧭 COGNITIVE LAYER (V9)
    # =========================================================
    def update_memory(self, msg):
        node = msg.get("node_id")
        self.memory[node] = {
            "last_msg": msg,
            "timestamp": time.time()
        }

        # simple system health decay model
        self.system_health = min(1.0, self.system_health + 0.001)

    # =========================================================
    # 📡 MESSAGE HANDLER
    # =========================================================
    def handle_message(self, msg, addr):

        # 🔐 reject spoofed nodes
        if not self.verify_signature(msg):
            print("[SECURITY] Rejected spoofed packet")
            return

        node = msg.get("node_id")

        # 🤝 enrollment
        if msg.get("type") == "enroll_request":
            self.handle_enroll(msg, addr)
            return

        # 🌐 discovery
        if msg.get("type") == "lan_discovery":
            self.discovery_cache[node] = addr
            return

        # 🧠 heartbeat
        if msg.get("type") in ["heartbeat", "ping", "cluster_ping"]:
            self.peers[node] = {
                "addr": addr,
                "last_seen": time.time()
            }

            self.update_memory(msg)

        print("[SWARM RX]", msg)

    # =========================================================
    # 📡 LISTENER LOOP
    # =========================================================
    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(65535)

            try:
                msg = json.loads(data.decode())
                self.handle_message(msg, addr)
            except:
                continue

    # =========================================================
    # 🚀 HEARTBEAT LOOP
    # =========================================================
    def heartbeat(self):
        while True:
            msg = {
                "node_id": self.node_id,
                "type": "heartbeat",
                "system_health": self.system_health,
                "timestamp": time.time()
            }

            msg["sig"] = self.sign(msg)

            best = self.best_peer()
            if best:
                addr = self.peers[best]["addr"]
                self.sock.sendto(json.dumps(msg).encode(), addr)

            print("[SWARM TX] heartbeat")
            time.sleep(3)

    # =========================================================
    # 🚀 START SYSTEM
    # =========================================================
    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.heartbeat, daemon=True).start()

        print("[OMEGA SWARM OS RUNNING]")
        while True:
            time.sleep(10)


if __name__ == "__main__":
    OmegaSwarmOS(port=6000).start()
