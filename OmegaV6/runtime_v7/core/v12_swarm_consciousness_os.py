import socket
import json
import time
import threading
import uuid

# =========================
# 🧠 V12 SWARM CONSCIOUSNESS OS
# =========================

class SwarmConsciousnessV12:
    def __init__(self, port=6050):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        # 🧠 CORE CONSCIOUS STATE
        self.nodes = {}
        self.memory_graph = {}   # event -> connections
        self.reflection_log = []

        self.node_id = str(uuid.uuid4())[:12]

        print(f"[V12] SWARM CONSCIOUSNESS ONLINE | node={self.node_id}")

    # -------------------------
    # 🧠 STORE MEMORY NODE
    # -------------------------
    def store_memory(self, event):
        eid = str(uuid.uuid4())[:8]

        self.memory_graph[eid] = {
            "event": event,
            "weight": 1.0,
            "links": []
        }

        # connect to previous memory (temporal chain)
        if len(self.memory_graph) > 1:
            prev = list(self.memory_graph.keys())[-2]
            self.memory_graph[prev]["links"].append(eid)

    # -------------------------
    # 🔁 REFLECTION ENGINE
    # -------------------------
    def reflect(self):
        if not self.memory_graph:
            return

        strongest = max(
            self.memory_graph.items(),
            key=lambda x: x[1]["weight"]
        )

        self.reflection_log.append({
            "focus": strongest[0],
            "event": strongest[1]["event"],
            "timestamp": time.time()
        })

        # reinforce memory
        strongest[1]["weight"] += 0.1

        print(f"[V12 REFLECT] focus={strongest[0]} weight={strongest[1]['weight']}")

    # -------------------------
    # 🌐 PROCESS MESSAGE
    # -------------------------
    def process(self, msg, addr):
        node = msg.get("node_id", "unknown")

        if node not in self.nodes:
            self.nodes[node] = {
                "seen": 0,
                "strength": 1.0
            }

        self.nodes[node]["seen"] += 1

        # store in cognitive memory graph
        self.store_memory(msg)

        print(f"[V12 EVENT] {msg}")

    # -------------------------
    # 🌐 LISTENER LOOP
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
    # 🔁 REFLECTION LOOP
    # -------------------------
    def reflection_loop(self):
        while True:
            time.sleep(5)
            self.reflect()

    # -------------------------
    # 🚀 START SYSTEM
    # -------------------------
    def start(self):
        print("[V12] STARTING SWARM CONSCIOUSNESS")

        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.reflection_loop, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(10)
            print(
                f"[V12 STATUS] nodes={len(self.nodes)} "
                f"memory={len(self.memory_graph)} reflections={len(self.reflection_log)}"
            )


if __name__ == "__main__":
    SwarmConsciousnessV12().start()
