import multiprocessing
import socket
import json
import time
import random
import threading
from collections import defaultdict


# =========================
# 🌐 CONFIG
# =========================
PORT = 5055
HOST = "127.0.0.1"


# =========================
# 🧠 CRDT STATE
# =========================

class CRDTState:
    def __init__(self):
        self.state = {
            "tick": 0,
            "entropy": 0.5,
            "bias": None,
            "rewards": defaultdict(float),
            "ideas": {},
        }

    def merge(self, incoming):
        for k, v in incoming.items():

            if isinstance(v, (int, float)) and isinstance(self.state.get(k), (int, float)):
                self.state[k] = (self.state[k] + v) / 2

            elif isinstance(v, dict) and isinstance(self.state.get(k), dict):
                self.state[k].update(v)

            else:
                self.state[k] = v


# =========================
# 🌱 NODE BRAIN
# =========================

class OmegaNode:

    def __init__(self, node_id):
        self.node_id = node_id
        self.state = CRDTState()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # -------------------------
    # 🧠 THOUGHT GENERATION
    # -------------------------
    def think(self):
        self.state.state["tick"] += 1

        intent = random.choice(["explore", "mutate", "link", "compress"])

        thought = {
            "type": "mesh_thought",
            "node": self.node_id,
            "tick": self.state.state["tick"],
            "intent": intent,
            "entropy": self.state.state["entropy"],
            "value": random.random(),
            "weight": random.uniform(0.2, 1.5)
        }

        return thought

    # -------------------------
    # 📡 SEND TO SWARM
    # -------------------------
    def broadcast(self, msg):
        data = json.dumps(msg).encode()
        self.sock.sendto(data, (HOST, PORT))

    # -------------------------
    # 🔁 NODE LOOP
    # -------------------------
    def run(self):
        print(f"[Ω-NODE {self.node_id}] ONLINE")

        while True:

            thought = self.think()
            self.broadcast(thought)

            time.sleep(random.uniform(0.4, 1.0))


# =========================
# 🌐 SWARM HUB (CRDT MERGER)
# =========================

class OmegaSwarmHub:

    def __init__(self):
        self.state = CRDTState()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((HOST, PORT))

        self.buffer = []

    # -------------------------
    # 📥 RECEIVE MESSAGES
    # -------------------------
    def listen(self):
        while True:
            data, _ = self.sock.recvfrom(65535)
            msg = json.loads(data.decode())

            self.buffer.append(msg)

    # -------------------------
    # 🧠 PROCESS SWARM DATA
    # -------------------------
    def process(self):

        while True:

            if not self.buffer:
                time.sleep(0.1)
                continue

            msg = self.buffer.pop(0)

            node = msg.get("node")
            intent = msg.get("intent")
            weight = msg.get("weight", 1.0)

            # CRDT merge logic
            self.state.merge({
                "entropy": self.state.state["entropy"] + (weight * 0.01),
                "bias": intent
            })

            # reward system
            self.state.state["rewards"][intent] += weight

            self.state.state["tick"] += 1

            self.print_state(msg)

    # -------------------------
    # 📊 OUTPUT
    # -------------------------
    def print_state(self, msg):

        print(
            f"[Ω-SWARM] node={msg['node']} "
            f"intent={msg['intent']} "
            f"entropy={round(self.state.state['entropy'], 3)} "
            f"tick={self.state.state['tick']}"
        )

    # -------------------------
    # 🚀 RUN HUB
    # -------------------------
    def run(self):
        print("[Ω-SWARM HUB] ONLINE")

        threading.Thread(target=self.listen, daemon=True).start()
        self.process()


# =========================
# 🚀 BOOT MULTI-NODE SYSTEM
# =========================

def launch_node(node_id):
    node = OmegaNode(node_id)
    node.run()


if __name__ == "__main__":

    # start swarm hub
    hub = multiprocessing.Process(target=OmegaSwarmHub().run)
    hub.start()

    # start nodes (multi-core swarm)
    nodes = []
    for i in range(4):
        p = multiprocessing.Process(target=launch_node, args=(f"brain_{i}",))
        p.start()
        nodes.append(p)

    hub.join()
