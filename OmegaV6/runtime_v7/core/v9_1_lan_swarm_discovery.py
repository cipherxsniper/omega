import socket
import threading
import time
import json
import hashlib


# ==============================
# V9.1 LAN SWARM DISCOVERY
# SAFE OPT-IN MESH ONLY
# ==============================

class LanSwarmV91:
    def __init__(self, port=6011):
        self.port = port
        self.running = True

        # discovered peers
        self.peers = {}        # ip -> metadata
        self.topology = {}     # node graph

        # identity
        self.node_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", self.port))

        print(f"[V9.1] LAN Swarm Discovery ONLINE | node={self.node_id}")

    # ==============================
    # 🔐 SAFE HANDSHAKE SYSTEM
    # ==============================
    def handshake(self, payload, addr):
        if payload.get("type") != "lan_hello":
            return

        peer_id = payload.get("node_id")
        if not peer_id:
            return

        self.peers[addr[0]] = {
            "node_id": peer_id,
            "last_seen": time.time(),
            "port": addr[1]
        }

        self.topology[peer_id] = addr[0]

        print(f"[V9.1 HANDSHAKE] {peer_id} @ {addr[0]}")

    # ==============================
    # 📡 LISTENER
    # ==============================
    def listen(self):
        print("[V9.1] Listener active")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                payload = json.loads(data.decode())

                self.handshake(payload, addr)

                print("[V9.1 RX]", payload)

            except Exception:
                pass

    # ==============================
    # 🌐 LAN DISCOVERY BROADCAST
    # SAFE LOCAL SUBNET ANNOUNCEMENT
    # ==============================
    def broadcast(self):
        while self.running:
            try:
                msg = {
                    "node_id": self.node_id,
                    "type": "lan_hello",
                    "timestamp": time.time()
                }

                data = json.dumps(msg).encode()

                # SAFE BROADCAST ONLY (no scanning)
                self.sock.sendto(data, ("127.0.0.1", self.port))

                print("[V9.1 TX] lan_hello")

            except Exception as e:
                print("[V9.1 ERROR]", e)

            time.sleep(5)

    # ==============================
    # 🧠 TOPOLOGY VIEW
    # ==============================
    def show_topology(self):
        while self.running:
            time.sleep(10)
            print("\n[V9.1 TOPOLOGY]")
            for node, ip in self.topology.items():
                print(f" - {node[:8]} -> {ip}")
            print("")

    # ==============================
    # 🚀 START SYSTEM
    # ==============================
    def start(self):
        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.broadcast, daemon=True)
        t3 = threading.Thread(target=self.show_topology, daemon=True)

        t1.start()
        t2.start()
        t3.start()

        print("[V9.1] SYSTEM RUNNING")

        while True:
            time.sleep(5)


if __name__ == "__main__":
    LanSwarmV91().start()
