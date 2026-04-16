import socket
import json
import time
import threading
import uuid
import hmac
import hashlib

# =========================
# 🔐 V15 SECURE SWARM OS
# =========================

SECRET_KEY = b"OMEGA_SWARM_V15_SECRET"

class SecureCognitiveSwarmV15:
    def __init__(self, port=6080):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = self._generate_node_id()

        # 🧠 TRUST SYSTEM
        self.trusted_nodes = set()
        self.event_log = []

        print(f"[V15] SECURE SWARM ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # 🧬 NODE ID
    # -------------------------
    def _generate_node_id(self):
        raw = str(uuid.uuid4()).encode()
        return hashlib.sha256(raw).hexdigest()[:16]

    # -------------------------
    # 🔐 SIGN MESSAGE
    # -------------------------
    def sign(self, data: dict):
        raw = json.dumps(data, sort_keys=True).encode()
        return hmac.new(SECRET_KEY, raw, hashlib.sha256).hexdigest()

    # -------------------------
    # 🔐 VERIFY MESSAGE
    # -------------------------
    def verify(self, msg):
        sig = msg.get("sig")
        if not sig:
            return False

        data = {k: msg[k] for k in msg if k != "sig"}
        expected = self.sign(data)

        return hmac.compare_digest(sig, expected)

    # -------------------------
    # 🌐 PROCESS MESSAGE
    # -------------------------
    def process(self, msg, addr):
        if not self.verify(msg):
            print(f"[V15 REJECTED] spoofed packet from {addr}")
            return

        node = msg.get("node_id")

        if node:
            self.trusted_nodes.add(node)

        self.event_log.append(msg)

        print(f"[V15 ACCEPTED] {msg}")

    # -------------------------
    # 🌐 LISTENER
    # -------------------------
    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(4096)

            try:
                msg = json.loads(data.decode())
            except:
                continue

            self.process(msg, addr)

    # -------------------------
    # 📡 SEND HEARTBEAT
    # -------------------------
    def heartbeat(self):
        while True:
            payload = {
                "node_id": self.node_id,
                "type": "heartbeat",
                "timestamp": time.time()
            }

            payload["sig"] = self.sign(payload)

            self.sock.sendto(
                json.dumps(payload).encode(),
                ("127.0.0.1", self.port)
            )

            time.sleep(5)

    # -------------------------
    # 🚀 START
    # -------------------------
    def start(self):
        print("[V15] STARTING SECURE SWARM")

        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(10)
            print(
                f"[V15 STATUS] trusted_nodes={len(self.trusted_nodes)} "
                f"events={len(self.event_log)}"
            )


if __name__ == "__main__":
    SecureCognitiveSwarmV15().start()
