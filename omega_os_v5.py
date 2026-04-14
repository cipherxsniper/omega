import random
import time
import json
import os
import uuid
from collections import defaultdict

# optional ZeroMQ
try:
    import zmq
    ZMQ_AVAILABLE = True
except:
    ZMQ_AVAILABLE = False


# =========================================================
# 🧠 CRDT-STYLE IDENTITY GRAPH (MERGEABLE STATE)
# =========================================================
class CRDTGraph:
    def __init__(self, path="omega_v5_graph.json"):
        self.path = path
        self.nodes = {}   # id -> state
        self.edges = defaultdict(set)
        self.version = 0
        self.load()

    # -----------------------------
    # CREATE IDEA NODE
    # -----------------------------
    def create_node(self):
        nid = str(uuid.uuid4())[:8]

        self.nodes[nid] = {
            "energy": random.uniform(0.5, 1.2),
            "fitness": 0.0,
            "timestamp": time.time()
        }

        return nid

    # -----------------------------
    # LINK NODES
    # -----------------------------
    def link(self, a, b):
        self.edges[a].add(b)

    # -----------------------------
    # CRDT MERGE (CORE OF V5)
    # -----------------------------
    def merge(self, incoming):
        for nid, data in incoming.get("nodes", {}).items():
            if nid not in self.nodes:
                self.nodes[nid] = data
            else:
                # LWW + energy dominance merge
                self.nodes[nid]["energy"] = max(
                    self.nodes[nid]["energy"],
                    data["energy"]
                )
                self.nodes[nid]["fitness"] = (
                    self.nodes[nid]["fitness"] + data["fitness"]
                ) / 2

        for a, bs in incoming.get("edges", {}).items():
            self.edges[a].update(bs)

    # -----------------------------
    # MUTATION
    # -----------------------------
    def evolve(self):
        for n in self.nodes:
            self.nodes[n]["energy"] *= (0.99 + random.uniform(-0.01, 0.02))
            self.nodes[n]["fitness"] += random.uniform(-0.01, 0.02)

    # -----------------------------
    # SAVE / LOAD
    # -----------------------------
    def save(self):
        with open(self.path, "w") as f:
            json.dump({
                "nodes": self.nodes,
                "edges": {k: list(v) for k, v in self.edges.items()}
            }, f, indent=2)

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    data = json.load(f)
                    self.nodes = data.get("nodes", {})
                    self.edges = defaultdict(set, {
                        k: set(v) for k, v in data.get("edges", {}).items()
                    })
            except:
                pass


# =========================================================
# 🧠 Ω-LANG COMPILER (SELF-MUTATING INSTRUCTION LAYER)
# =========================================================
class OmegaLangV5:
    def execute(self, instruction, graph: CRDTGraph):
        parts = instruction.split()

        if not parts:
            return

        cmd = parts[0]

        if cmd == "SPAWN":
            graph.create_node()

        elif cmd == "LINK":
            if len(graph.nodes) > 1:
                a, b = random.sample(list(graph.nodes.keys()), 2)
                graph.link(a, b)

        elif cmd == "BOOST":
            for n in graph.nodes:
                graph.nodes[n]["energy"] += 0.05

        elif cmd == "DAMPEN":
            for n in graph.nodes:
                graph.nodes[n]["energy"] *= 0.98


# =========================================================
# 🌐 DISTRIBUTED TRANSPORT LAYER (ZEROMQ READY)
# =========================================================
class Transport:
    def __init__(self, port=5555):
        self.port = port
        self.context = None
        self.socket = None

        if ZMQ_AVAILABLE:
            self.context = zmq.Context()
            self.socket = self.context.socket(zmq.PAIR)
            self.socket.bind(f"tcp://127.0.0.1:{port}")

    def send(self, msg):
        if self.socket:
            self.socket.send_json(msg)

    def recv(self):
        if self.socket:
            try:
                return self.socket.recv_json(flags=zmq.NOBLOCK)
            except:
                return None
        return None


# =========================================================
# 🧠 OMEGA NODE (DISTRIBUTED AGENT)
# =========================================================
class OmegaNode:
    def __init__(self, node_id, graph, transport):
        self.id = node_id
        self.graph = graph
        self.transport = transport
        self.lang = OmegaLangV5()

    def step(self):
        # -------------------------
        # local evolution
        # -------------------------
        if random.random() < 0.3:
            self.lang.execute("SPAWN", self.graph)

        if random.random() < 0.2:
            self.lang.execute("LINK", self.graph)

        # -------------------------
        # reinforcement
        # -------------------------
        for n in self.graph.nodes:
            self.graph.nodes[n]["fitness"] += random.uniform(-0.01, 0.02)

        self.graph.evolve()

        # -------------------------
        # broadcast state (CRDT sync)
        # -------------------------
        self.transport.send({
            "nodes": self.graph.nodes,
            "edges": {k: list(v) for k, v in self.graph.edges.items()}
        })

        # -------------------------
        # receive remote updates
        # -------------------------
        incoming = self.transport.recv()
        if incoming:
            self.graph.merge(incoming)


# =========================================================
# 🧠 OMEGAOS v5 KERNEL
# =========================================================
class OmegaOSv5:
    def __init__(self):
        self.graph = CRDTGraph()
        self.transport = Transport()
        self.nodes = [
            OmegaNode(f"node_{i}", self.graph, self.transport)
            for i in range(4)
        ]
        self.tick = 0

    def run(self):
        print("[Ω-OS v5] Distributed Cognitive Network ONLINE")
        print(f"[Ω-OS v5] ZMQ={'ON' if ZMQ_AVAILABLE else 'OFF (local mode)'}")

        while True:
            self.tick += 1

            for node in self.nodes:
                node.step()

            # global stabilization
            if self.tick % 10 == 0:
                self.graph.save()

            # metrics
            if self.tick % 5 == 0:
                avg_energy = (
                    sum(n["energy"] for n in self.graph.nodes.values())
                    / max(1, len(self.graph.nodes))
                )

                print(
                    f"[Ω-v5] tick={self.tick} "
                    f"nodes={len(self.graph.nodes)} "
                    f"avg_energy={avg_energy:.3f}"
                )

            time.sleep(0.4)


# =========================================================
# BOOT
# =========================================================
if __name__ == "__main__":
    OmegaOSv5().run()
