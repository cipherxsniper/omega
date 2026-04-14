import multiprocessing
import socket
import json
import time
import random
import threading
import os
from collections import defaultdict


# =========================
# 🌐 CONFIG
# =========================
HOST = "127.0.0.1"
PORT = 5060
MEMORY_FILE = "omega_identity_graph_v11.json"


# =========================
# 🧬 IDENTITY GRAPH (PERSISTENT)
# =========================

class IdentityGraph:

    def __init__(self):
        self.state = self.load()

    def load(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, "r") as f:
                    return json.load(f)
            except:
                pass

        return {
            "nodes": {},
            "edges": {},
            "global_entropy": 0.5,
            "tick": 0
        }

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.state, f, indent=2)

    # -------------------------
    # 🧠 UPDATE NODE IDENTITY
    # -------------------------
    def update_node(self, node_id, intent, reward):

        nodes = self.state["nodes"]

        if node_id not in nodes:
            nodes[node_id] = {
                "role": random.choice(["explorer", "mutator", "linker", "compressor"]),
                "strength": 1.0,
                "experience": 0,
                "bias": intent,
                "reward": 0
            }

        node = nodes[node_id]

        # learning update
        node["reward"] += reward
        node["experience"] += 1
        node["bias"] = intent

        # role evolution
        if node["reward"] > 10:
            node["role"] = random.choice(["explorer", "mutator", "linker", "compressor"])
            node["reward"] *= 0.5

        # strength evolves
        node["strength"] = min(2.0, 0.5 + node["reward"] * 0.1)

    # -------------------------
    # 🌐 GLOBAL ENTROPY DRIFT
    # -------------------------
    def drift(self, value):
        self.state["global_entropy"] += value
        self.state["global_entropy"] *= 0.99

    def tick(self):
        self.state["tick"] += 1


# =========================
# 🧠 NODE
# =========================

class OmegaNode:

    def __init__(self, node_id):
        self.node_id = node_id
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def think(self):

        return {
            "node": self.node_id,
            "intent": random.choice(["explore", "mutate", "link", "compress"]),
            "value": random.random(),
            "reward": random.uniform(0.1, 1.0),
            "entropy": random.uniform(0.3, 0.9),
            "tick": time.time()
        }

    def send(self, msg):
        self.sock.sendto(json.dumps(msg).encode(), (HOST, PORT))

    def run(self):
        print(f"[Ω-NODE {self.node_id}] ONLINE")

        while True:
            msg = self.think()
            self.send(msg)
            time.sleep(random.uniform(0.3, 0.9))


# =========================
# 🌐 SWARM HUB
# =========================

class OmegaSwarm:

    def __init__(self):
        self.graph = IdentityGraph()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))

        self.buffer = []

    # -------------------------
    # 📡 LISTENER
    # -------------------------
    def listen(self):
        while True:
            data, _ = self.sock.recvfrom(65535)
            self.buffer.append(json.loads(data.decode()))

    # -------------------------
    # 🧠 PROCESS EVOLUTION
    # -------------------------
    def process(self):

        while True:

            if not self.buffer:
                time.sleep(0.05)
                continue

            msg = self.buffer.pop(0)

            node_id = msg["node"]
            intent = msg["intent"]
            reward = msg["reward"]
            entropy = msg["entropy"]

            # 🧬 update identity graph
            self.graph.update_node(node_id, intent, reward)

            # 🌐 global drift
            self.graph.drift(entropy * 0.01)
            self.graph.tick()

            self.print_state(msg)

            # 💾 persistence every cycle
            if self.graph.state["tick"] % 10 == 0:
                self.graph.save()

    # -------------------------
    # 📊 OUTPUT
    # -------------------------
    def print_state(self, msg):

        node = self.graph.state["nodes"].get(msg["node"], {})

        print(
            f"[Ω-v11] node={msg['node']} "
            f"role={node.get('role','?')} "
            f"intent={msg['intent']} "
            f"reward={round(msg['reward'],3)} "
            f"global_entropy={round(self.graph.state['global_entropy'],3)} "
            f"tick={self.graph.state['tick']}"
        )

    def run(self):
        print("[Ω-MESH v11] IDENTITY GRAPH SWARM ONLINE")

        threading.Thread(target=self.listen, daemon=True).start()
        self.process()


# =========================
# 🚀 BOOT
# =========================

def launch_node(node_id):
    OmegaNode(node_id).run()


if __name__ == "__main__":

    hub = multiprocessing.Process(target=OmegaSwarm().run)
    hub.start()

    nodes = []
    for i in range(5):
        p = multiprocessing.Process(target=launch_node, args=(f"brain_{i}",))
        p.start()
        nodes.append(p)

    hub.join()
