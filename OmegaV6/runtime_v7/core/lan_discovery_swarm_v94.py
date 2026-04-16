import socket
import json
import threading
import time
import ipaddress

PORT = 6009
BROADCAST_PORT = 6009
DISCOVERY_INTERVAL = 5

class LanSwarmV94:
    def __init__(self):
        self.node_id = self.generate_node_id()
        self.peers = {}  # ip -> last_seen
        self.running = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0", PORT))

    def generate_node_id(self):
        return hex(int(time.time() * 1000000))[2:]

    # 🌐 BROADCAST SELF TO LAN
    def broadcast_presence(self):
        msg = {
            "node_id": self.node_id,
            "type": "lan_discovery",
            "timestamp": time.time()
        }

        data = json.dumps(msg).encode()

        self.sock.sendto(data, ("255.255.255.255", BROADCAST_PORT))

    # 📡 LISTEN FOR NODES
    def listen(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                msg = json.loads(data.decode())

                if msg.get("type") == "lan_discovery":
                    self.register_peer(addr[0], msg)

            except Exception:
                continue

    # 🤝 REGISTER PEER
    def register_peer(self, ip, msg):
        self.peers[ip] = time.time()
        print(f"[LAN DISCOVERY] peer={ip} node={msg.get('node_id')}")

    # 🧠 CLEAN OLD PEERS
    def cleanup(self):
        while self.running:
            now = time.time()
            self.peers = {
                ip: t for ip, t in self.peers.items()
                if now - t < 20
            }
            time.sleep(5)

    # 🚀 MAIN LOOP
    def start(self):
        print(f"[V9.4 LAN MESH] ONLINE | node={self.node_id}")

        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.cleanup, daemon=True).start()

        while self.running:
            self.broadcast_presence()
            print(f"[LAN MESH] peers={len(self.peers)}")
            time.sleep(DISCOVERY_INTERVAL)


if __name__ == "__main__":
    LanSwarmV94().start()
