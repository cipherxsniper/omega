import socket
import json
import time
import threading
import uuid
import hashlib

# =========================
# 🔐 V16 LIGHTWEIGHT CRYPTO SWARM
# (NO EXTERNAL DEPENDENCIES)
# =========================

class PublicKeySwarmV16:
    def __init__(self, port=6090):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = str(uuid.uuid4())[:12]

        # 🧠 TRUST REGISTRY
        self.trusted_nodes = set()
        self.event_log = []

        print(f"[V16-LITE] SWARM ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # 🔐 SIMPLE SIGNATURE (SHA256-BASED)
    # -------------------------
    def sign(self, data: dict):
        raw = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(raw + self.node_id.encode()).hexdigest()

    # -------------------------
    # 🔐 VERIFY SIGNATURE
    # -------------------------
    def verify(self, msg):
        sig = msg.get("sig")
        if not sig:
            return False

        data = {k: msg[k] for k in msg if k != "sig"}
        raw = json.dumps(data, sort_keys=True).encode()

        expected = hashlib.sha256(raw + msg.get("node_id","").encode()).hexdigest()

        return sig == expected

    # -------------------------
    # 🌐 PROCESS MESSAGE
    # -------------------------
    def process(self, msg, addr):
        if not self.verify(msg):
            print(f"[V16 REJECTED] invalid packet from {addr}")
            return

        node = msg.get("node_id")
        if node:
            self.trusted_nodes.add(node)

        self.event_log.append(msg)

        print(f"[V16 ACCEPTED] {msg}")

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
    # 📡 HEARTBEAT
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
        print("[V16-LITE] STARTING SWARM")

        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(10)
            print(f"[V16 STATUS] trusted={len(self.trusted_nodes)} events={len(self.event_log)}")


if __name__ == "__main__":
    PublicKeySwarmV16().start()
