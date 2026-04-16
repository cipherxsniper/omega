import socket
import json
import time
import threading
import random

# =========================
# 🧠 V11 SWARM INTELLIGENCE OS
# =========================

class SwarmIntelligenceV11:
    def __init__(self, port=6040):
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", self.port))

        # 🧠 SWARM STATE
        self.nodes = {}          # node_id -> stats
        self.task_queue = []
        self.memory = []         # collective experience

        print(f"[V11] SWARM INTELLIGENCE ONLINE | port={self.port}")

    # -------------------------
    # 📊 UPDATE NODE PROFILE
    # -------------------------
    def update_node(self, node_id, latency=1.0):
        if node_id not in self.nodes:
            self.nodes[node_id] = {
                "score": 1.0,
                "tasks": 0,
                "latency": latency
            }
        else:
            n = self.nodes[node_id]
            n["tasks"] += 1
            n["score"] += max(0.01, 1.0 - latency)

    # -------------------------
    # 🧠 SELECT BEST NODE
    # -------------------------
    def select_node(self):
        if not self.nodes:
            return None

        ranked = sorted(
            self.nodes.items(),
            key=lambda x: (x[1]["score"] / (x[1]["latency"] + 0.1)),
            reverse=True
        )

        return ranked[0][0]

    # -------------------------
    # 📦 PROCESS TASK
    # -------------------------
    def process_task(self, task):
        node = self.select_node()

        if not node:
            print("[V11] NO NODES AVAILABLE")
            return

        self.memory.append({
            "task": task,
            "assigned_to": node,
            "timestamp": time.time()
        })

        self.update_node(node)

        print(f"[V11 TASK] {task} → {node}")

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

            node_id = msg.get("node_id", f"node_{addr[1]}")

            # register node if new
            if node_id not in self.nodes:
                self.nodes[node_id] = {
                    "score": random.uniform(0.5, 1.5),
                    "tasks": 0,
                    "latency": random.uniform(0.1, 1.0)
                }

            # treat message as task or heartbeat
            if msg.get("type") == "task":
                self.process_task(msg)

            self.update_node(node_id)

    # -------------------------
    # 🧠 SIMULATED TASK GENERATOR
    # -------------------------
    def task_generator(self):
        tasks = ["analyze", "route", "sync", "compute", "verify"]

        while True:
            task = {
                "type": "task",
                "task": random.choice(tasks),
                "node_id": "local_generator"
            }

            self.sock.sendto(
                json.dumps(task).encode(),
                ("127.0.0.1", self.port)
            )

            time.sleep(4)

    # -------------------------
    # 🚀 START
    # -------------------------
    def start(self):
        print("[V11] STARTING SWARM INTELLIGENCE")

        t1 = threading.Thread(target=self.listen, daemon=True)
        t2 = threading.Thread(target=self.task_generator, daemon=True)

        t1.start()
        t2.start()

        while True:
            time.sleep(10)
            print(f"[V11 STATUS] nodes={len(self.nodes)} memory={len(self.memory)}")


if __name__ == "__main__":
    SwarmIntelligenceV11().start()
