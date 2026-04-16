import socket
import json
import time
import threading
import hashlib

class CognitiveSwarmV96:

    def __init__(self, port=6016):
        self.port = port
        self.node_id = self._id()

        # 🧠 LOCAL + SWARM MEMORY
        self.local_memory = []
        self.swarm_memory = {}

        # 🌐 PEERS
        self.peers = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0", self.port))

        print(f"[V9.6 COGNITIVE SWARM] ONLINE | node={self.node_id}")

    # 🧬 NODE ID
    def _id(self):
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]

    # 🧠 ADD LOCAL MEMORY
    def remember(self, event):
        entry = {
            "event": event,
            "timestamp": time.time(),
            "node": self.node_id
        }
        self.local_memory.append(entry)

        # keep bounded
        self.local_memory = self.local_memory[-50:]

        # propagate to swarm
        self.broadcast_memory(entry)

    # 🌐 BROADCAST MEMORY
    def broadcast_memory(self, entry):
        msg = {
            "type": "swarm_memory_update",
            "data": entry
        }

        self.sock.sendto(
            json.dumps(msg).encode(),
            ("255.255.255.255", self.port)
        )

    # 📡 LISTEN LOOP
    def listen(self):
        while True:
            data, addr = self.sock.recvfrom(4096)

            try:
                msg = json.loads(data.decode())
            except:
                continue

            if msg.get("type") == "swarm_memory_update":
                self.integrate(msg["data"], addr[0])

    # 🧠 INTEGRATE SWARM MEMORY
    def integrate(self, data, ip):
        key = f"{data['node']}:{data['timestamp']}"

        if key not in self.swarm_memory:
            self.swarm_memory[key] = data

            print(f"[SWARM MEMORY] synced from {ip} -> {data['event']}")

    # 🚀 DEMO LOOP
    def thinker(self):
        while True:
            self.remember(f"heartbeat from {self.node_id}")
            time.sleep(5)

    # 🚀 START
    def start(self):
        threading.Thread(target=self.listen, daemon=True).start()
        threading.Thread(target=self.thinker, daemon=True).start()

        while True:
            print(f"[MEMORY] local={len(self.local_memory)} swarm={len(self.swarm_memory)}")
            time.sleep(5)


if __name__ == "__main__":
    CognitiveSwarmV96().start()
