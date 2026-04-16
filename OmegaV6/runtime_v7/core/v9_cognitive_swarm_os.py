import socket
import threading
import time
import json
import hashlib


# ==============================
# V9 COGNITIVE SWARM OS
# ==============================

class CognitiveSwarmV9:
    def __init__(self, port=6010):
        self.port = port
        self.running = True

        # distributed state
        self.memory = {}
        self.peer_trust = {}
        self.peers = {}

        # identity security
        self.secret_key = "OMEGA_SWARM_KEY"

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        print("[V9] Cognitive Swarm OS ONLINE", flush=True)

    # ==============================
    # 🔐 SIGNATURE SYSTEM
    # ==============================
    def sign(self, data: str):
        return hashlib.sha256((data + self.secret_key).encode()).hexdigest()

    def verify(self, payload):
        if "sig" not in payload:
            return False

        raw = json.dumps({
            "node_id": payload.get("node_id"),
            "type": payload.get("type"),
            "data": payload.get("data", "")
        }, sort_keys=True)

        expected = self.sign(raw)
        return expected == payload["sig"]

    # ==============================
    # 🧠 MEMORY SYSTEM
    # ==============================
    def update_memory(self, node_id, payload):
        if node_id not in self.memory:
            self.memory[node_id] = []

        self.memory[node_id].append({
            "data": payload,
            "time": time.time()
        })

    # ==============================
    # 🌐 PEER DISCOVERY (SAFE LAN SIM)
    # ==============================
    def discover_peers(self):
        # safe local simulation (no real scanning abuse)
        base_ip = "127.0.0."
        for i in range(1, 5):
            ip = base_ip + str(i)
            self.peers[ip] = time.time()

    # ==============================
    # 🔐 TRUST SYSTEM
    # ==============================
    def update_trust(self, node_id):
        self.peer_trust[node_id] = min(
            1.0,
            self.peer_trust.get(node_id, 0.5) + 0.01
        )

    # ==============================
    # 📡 LISTENER
    # ==============================
    def listen(self):
        print("[V9] Listener active", flush=True)

        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                node_id = payload.get("node_id")

                # 🔐 anti-spoof check
                if not self.verify(payload):
                    print("[V9] REJECTED FAKE NODE", payload, flush=True)
                    continue

                # 🧠 memory update
                self.update_memory(node_id, payload)
                self.update_trust(node_id)

                print("[V9 RX]", payload, flush=True)

                # log persistence
                with open("logs/v9_swarm.log", "a") as f:
                    f.write(json.dumps(payload) + "\n")

            except Exception:
                pass

    # ==============================
    # 💓 COGNITIVE HEARTBEAT
    # ==============================
    def heartbeat(self):
        while self.running:
            try:
                payload = {
                    "node_id": "local_v9",
                    "type": "heartbeat",
                    "data": "cognitive_sync"
                }

                raw = json.dumps(payload, sort_keys=True)
                payload["sig"] = self.sign(raw)

                data = json.dumps(payload).encode()

                self.sock.sendto(data, ("127.0.0.1", self.port))

                print("[V9 TX] heartbeat", flush=True)

            except Exception as e:
                print("[V9 ERROR]", e, flush=True)

            time.sleep(3)

    # ==============================
    # 🧠 START SYSTEM
    # ==============================
    def start(self):
        self.discover_peers()

        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.heartbeat, daemon=True)

        t1.start()
        t2.start()

        print("[V9] SYSTEM RUNNING", flush=True)

        while True:
            time.sleep(5)


if __name__ == "__main__":
    CognitiveSwarmV9().start()
