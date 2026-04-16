import socket
import json
import time
import hashlib
import hmac
import threading
import uuid

# =========================
# 🔐 CRYPTO SWARM OS V10
# =========================

class CryptoSwarmOSV10:
    def __init__(self, port=6030):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        self.key = b"OMEGA_V10_MASTER_KEY"

        self.node_id = str(uuid.uuid4())[:16]

        self.event_chain = []   # 🔗 immutable swarm history
        self.reputation = {}    # 📊 node trust scores

        print(f"[V10 CRYPTO SWARM] ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # 🔐 SIGN EVENT
    # -------------------------
    def sign(self, event):
        raw = json.dumps(event, sort_keys=True).encode()
        return hmac.new(self.key, raw, hashlib.sha256).hexdigest()

    # -------------------------
    # 🔐 VERIFY EVENT
    # -------------------------
    def verify(self, event):
        sig = event.get("sig")
        if not sig:
            return False

        raw = {k: event[k] for k in event if k != "sig"}
        expected = self.sign(raw)

        return hmac.compare_digest(sig, expected)

    # -------------------------
    # 🧱 APPLY EVENT
    # -------------------------
    def apply_event(self, event, addr):
        node = event.get("node_id", "unknown")

        # 📊 reputation system
        self.reputation[node] = self.reputation.get(node, 0) + 1

        self.event_chain.append({
            "event": event,
            "addr": addr,
            "timestamp": time.time()
        })

        print(f"[V10 EVENT] {event}")

    # -------------------------
    # 🌐 LISTENER LOOP
    # -------------------------
    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(4096)

            try:
                event = json.loads(data.decode())
            except:
                continue

            # 🔐 reject invalid
            if not self.verify(event):
                print("[V10] REJECTED INVALID SIGNATURE")
                continue

            self.apply_event(event, addr)

    # -------------------------
    # 📡 HEARTBEAT BROADCAST
    # -------------------------
    def broadcast_loop(self):
        while True:
            event = {
                "node_id": self.node_id,
                "type": "heartbeat",
                "timestamp": time.time()
            }

            event["sig"] = self.sign(event)

            self.sock.sendto(
                json.dumps(event).encode(),
                ("127.0.0.1", self.port)
            )

            time.sleep(3)

    # -------------------------
    # 🚀 START SYSTEM
    # -------------------------
    def start(self):
        print("[V10] CRYPTO SWARM STARTING")

        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.broadcast_loop, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(10)
            print(f"[V10 STATUS] events={len(self.event_chain)} | peers={len(self.reputation)}")


if __name__ == "__main__":
    CryptoSwarmOSV10().start()
