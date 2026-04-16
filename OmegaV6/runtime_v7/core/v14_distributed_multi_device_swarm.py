import socket
import json
import time
import threading
import uuid

# =========================
# 🌐 V14 DISTRIBUTED SWARM
# =========================

class DistributedSwarmV14:
    def __init__(self, port=6070):
        self.port = port

        # UDP socket (LAN capable)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        # 🧠 GLOBAL STATE
        self.node_id = str(uuid.uuid4())[:12]

        self.peers = set()
        self.global_events = {}   # event_id -> event
        self.global_edges = []    # (a,b,source_node)

        print(f"[V14] DISTRIBUTED SWARM ONLINE | node={self.node_id} | port={self.port}")

    # -------------------------
    # 🌐 BROADCAST EVENT
    # -------------------------
    def broadcast(self, event):
        msg = {
            "node_id": self.node_id,
            "type": "swarm_event",
            "event": event
        }

        # broadcast to LAN (simple local subnet assumption)
        for i in range(1, 255):
            try:
                self.sock.sendto(
                    json.dumps(msg).encode(),
                    (f"127.0.0.{i}", self.port)
                )
            except:
                pass

    # -------------------------
    # 🧠 PROCESS EVENT
    # -------------------------
    def process(self, msg, addr):
        node = msg.get("node_id")

        if node:
            self.peers.add(node)

        if msg.get("type") == "swarm_event":
            event = msg.get("event")

            eid = str(uuid.uuid4())[:8]
            self.global_events[eid] = {
                "event": event,
                "from": node,
                "timestamp": time.time()
            }

            print(f"[V14 EVENT] {node} → {event}")

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
    # 📡 SIMULATED LOCAL EVENTS
    # -------------------------
    def generator(self):
        events = ["compute", "route", "sync", "analyze"]

        while True:
            event = {
                "action": events[int(time.time()) % len(events)],
                "source": self.node_id
            }

            self.broadcast(event)
            time.sleep(5)

    # -------------------------
    # 🚀 START
    # -------------------------
    def start(self):
        print("[V14] STARTING DISTRIBUTED SWARM")

        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.generator, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(10)
            print(
                f"[V14 STATUS] peers={len(self.peers)} "
                f"events={len(self.global_events)}"
            )


if __name__ == "__main__":
    DistributedSwarmV14().start()
