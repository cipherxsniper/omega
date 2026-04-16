import socket
import json
import time
import threading
import uuid

# =========================
# 🌐 V17 LAN AUTO SWARM
# =========================

class LANAutoEnrollmentV17:
    def __init__(self, port=6100):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        self.node_id = str(uuid.uuid4())[:12]

        # 🧠 SWARM STATE
        self.peers = {}   # ip -> node_id
        self.active_nodes = set()

        print(f"[V17] LAN SWARM ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # 🔍 DISCOVERY BEACON
    # -------------------------
    def broadcast_probe(self):
        msg = {
            "type": "lan_probe",
            "node_id": self.node_id,
            "port": self.port
        }

        for i in range(1, 255):
            ip = f"127.0.0.{i}"
            try:
                self.sock.sendto(json.dumps(msg).encode(), (ip, self.port))
            except:
                pass

    # -------------------------
    # 🤝 HANDLE INCOMING MESSAGE
    # -------------------------
    def process(self, msg, addr):
        msg_type = msg.get("type")
        node_id = msg.get("node_id")

        if not node_id:
            return

        ip = addr[0]

        # 🧾 AUTO ENROLLMENT
        if msg_type == "lan_probe":
            self.peers[ip] = node_id
            self.active_nodes.add(node_id)

            # respond with acceptance
            response = {
                "type": "lan_ack",
                "node_id": self.node_id,
                "peer": node_id
            }

            self.sock.sendto(json.dumps(response).encode(), addr)

            print(f"[V17] ENROLLED NODE {node_id} @ {ip}")

        elif msg_type == "lan_ack":
            self.peers[ip] = node_id
            self.active_nodes.add(node_id)

            print(f"[V17] ACK RECEIVED FROM {node_id} @ {ip}")

        elif msg_type == "heartbeat":
            self.active_nodes.add(node_id)
            self.peers[ip] = node_id

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
            msg = {
                "type": "heartbeat",
                "node_id": self.node_id,
                "timestamp": time.time()
            }

            # broadcast heartbeat to swarm
            for i in range(1, 255):
                try:
                    self.sock.sendto(json.dumps(msg).encode(), (f"127.0.0.{i}", self.port))
                except:
                    pass

            time.sleep(5)

    # -------------------------
    # 🔍 PERIODIC DISCOVERY
    # -------------------------
    def discovery_loop(self):
        while True:
            self.broadcast_probe()
            time.sleep(10)

    # -------------------------
    # 🚀 START
    # -------------------------
    def start(self):
        print("[V17] STARTING AUTO-ENROLLMENT SWARM")

        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.heartbeat, daemon=True).start()
        threading.Thread(target=self.discovery_loop, daemon=True).start()

        while True:
            time.sleep(10)
            print(
                f"[V17 STATUS] peers={len(self.peers)} "
                f"active_nodes={len(self.active_nodes)}"
            )


if __name__ == "__main__":
    LANAutoEnrollmentV17().start()
