import socket
import threading
import time
import json
import hashlib
import uuid
import os


# =========================
# NODE IDENTITY (SECURE)
# =========================
class NodeIdentityV74:
    def __init__(self):
        self.seed = uuid.uuid4().hex
        self.hostname = socket.gethostname()
        self.created = time.time()

        self.node_id = self.generate_id()

    def generate_id(self):
        raw = f"{self.hostname}:{self.seed}:{self.created}".encode()
        return hashlib.sha256(raw).hexdigest()

    def sign(self, payload):
        raw = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

    def payload(self):
        return {
            "node_id": self.node_id,
            "hostname": self.hostname,
            "timestamp": time.time(),
            "type": "omega_v7_4_cluster_node"
        }


# =========================
# CLUSTER NODE V7.4
# =========================
class ClusterNodeV74:
    def __init__(self, port=6001):
        self.identity = NodeIdentityV74()

        self.port = port
        self.running = True

        self.peers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            self.sock.bind(("0.0.0.0", self.port))
        except OSError:
            self.port += 1
            self.sock.bind(("0.0.0.0", self.port))

        # SAFE LOCAL MODE ONLY
        self.targets = ["127.0.0.1"]

    # =========================
    # HEARTBEAT BROADCAST
    # =========================
    def broadcast(self):
        while self.running:
            try:
                payload = self.identity.payload()
                payload["sig"] = self.identity.sign(payload)

                data = json.dumps(payload).encode()

                for ip in self.targets:
                    self.sock.sendto(data, (ip, self.port))

                # self register (Termux-safe)
                self.peers[payload["node_id"]] = time.time()

            except Exception as e:
                print("[BROADCAST ERROR]", e)

            time.sleep(2)

    # =========================
    # RECEIVE PEERS
    # =========================
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                node_id = payload.get("node_id")
                sig = payload.get("sig")

                if node_id:
                    # verify signature (light trust check)
                    expected = hashlib.sha256(
                        json.dumps({k: payload[k] for k in payload if k != "sig"},
                                   sort_keys=True).encode()
                    ).hexdigest()

                    if sig == expected:
                        self.peers[node_id] = time.time()

                print("[V7.4 RX]", payload)

            except Exception:
                pass

    # =========================
    # CLEAN DEAD PEERS
    # =========================
    def cleanup(self):
        while self.running:
            now = time.time()
            self.peers = {
                k: v for k, v in self.peers.items()
                if now - v < 15
            }
            time.sleep(5)

    # =========================
    # HEARTBEAT MONITOR
    # =========================
    def monitor(self):
        while self.running:
            print({
                "node": self.identity.node_id[:12],
                "port": self.port,
                "peers": len(self.peers)
            })
            time.sleep(3)

    # =========================
    # SELF HEAL (BASIC DAEMON SAFETY)
    # =========================
    def watchdog(self):
        while self.running:
            try:
                if not self.sock:
                    print("[WATCHDOG] restarting socket")
                    self.__init__(self.port)
            except Exception:
                pass

            time.sleep(10)

    # =========================
    # START CLUSTER NODE
    # =========================
    def run(self):
        print("[Ω-V7.4] SAFE DISTRIBUTED CLUSTER ONLINE")

        threading.Thread(target=self.broadcast, daemon=True).start()
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.cleanup, daemon=True).start()
        threading.Thread(target=self.monitor, daemon=True).start()
        threading.Thread(target=self.watchdog, daemon=True).start()

        while True:
            time.sleep(1)


if __name__ == "__main__":
    ClusterNodeV74().run()
