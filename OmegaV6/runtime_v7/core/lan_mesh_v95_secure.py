import socket
import json
import time
import threading
import hmac
import hashlib

class SecureLanMeshV95:

    def __init__(self, key="OMEGA_SWARM_KEY_V95", port=6015):
        self.key = key
        self.port = port
        self.node_id = self.generate_node_id()

        self.peers = {}
        self.trust = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0", self.port))

        print(f"[V9.5 SECURE MESH] ONLINE | node={self.node_id}")

    # 🧬 NODE ID
    def generate_node_id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

    # 🔐 SIGN PACKET
    def sign(self, msg):
        raw = json.dumps(msg, sort_keys=True).encode()
        return hmac.new(self.key.encode(), raw, hashlib.sha256).hexdigest()

    # 🔐 VERIFY PACKET  ← THIS IS YOUR FUNCTION (correct place)
    def verify_signature(self, msg):
        sig = msg.get("sig")
        if not sig:
            return False

        raw = {k: msg[k] for k in msg if k != "sig"}

        expected = hmac.new(
            self.key.encode(),
            json.dumps(raw, sort_keys=True).encode(),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(sig, expected)

    # 🌐 BROADCAST
    def broadcast(self):
        msg = {
            "node_id": self.node_id,
            "type": "lan_secure_ping",
            "timestamp": time.time()
        }

        msg["sig"] = self.sign(msg)

        self.sock.sendto(
            json.dumps(msg).encode(),
            ("255.255.255.255", self.port)
        )

    # 📡 LISTEN
    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(4096)

            try:
                msg = json.loads(data.decode())
            except:
                continue

            # 🔐 SECURITY GATE (THIS IS THE KEY LINE)
            if not self.verify_signature(msg):
                print("[REJECTED] fake node detected")
                continue

            self.register_peer(addr[0], msg)

    # 🤝 REGISTER PEER
    def register_peer(self, ip, msg):
        self.peers[ip] = time.time()

        if ip not in self.trust:
            self.trust[ip] = 1.0

        print(f"[SECURE PEER] {ip} node={msg.get('node_id')}")

    # 🚀 RUN
    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()

        while True:
            self.broadcast()
            print(f"[MESH] peers={len(self.peers)}")
            time.sleep(5)


if __name__ == "__main__":
    SecureLanMeshV95().start()
