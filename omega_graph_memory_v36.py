import json
import os
import time
import threading
from collections import defaultdict
from omega_graph_memory_patch_atomic import _atomic_write
from omega_graph_memory_patch_init import ensure_graph_file
from omega_graph_memory_patch_queue import WRITE_QUEUE, start_writer_loop

GRAPH_FILE = "omega_graph_memory.json"
LOCK = threading.Lock()


# =========================
# 🧠 COGNITIVE GRAPH ENGINE V36
# =========================
class CognitiveGraphMemory:
    def __init__(self):
        self._ensure_graph()

    # -------------------------
    # INIT / SELF-HEAL
    # -------------------------
    def _ensure_graph(self):
        if not os.path.exists(GRAPH_FILE):
            self._atomic_write({
                "nodes": {},
                "edges": {},
                "meta": {
                    "created": time.time(),
                    "version": 36
                }
            })

    # -------------------------
    # SAFE LOAD
    # -------------------------
    def read(self):
        self._ensure_graph()

        with LOCK:
            try:
                with open(GRAPH_FILE, "r") as f:
                    data = json.load(f)

                if "nodes" not in data:
                    data["nodes"] = {}

                if "edges" not in data:
                    data["edges"] = {}

                return data

            except json.JSONDecodeError:
                # auto repair corrupted graph
                return {
                    "nodes": {},
                    "edges": {},
                    "meta": {"repaired": time.time()}
                }

    # -------------------------
    # ATOMIC WRITE
    # -------------------------
    def _atomic_write(self, data):
        tmp = GRAPH_FILE + ".tmp"

        with open(tmp, "w") as f:
            json.dump(data, f, separators=(",", ":"))

        os.replace(tmp, GRAPH_FILE)

    # -------------------------
    # NODE UPDATE (LEARNING SIGNAL)
    # -------------------------
    def update_node(self, node_id, signal_strength):
        graph = self.read()

        nodes = graph["nodes"]

        if node_id not in nodes:
            nodes[node_id] = {
                "activation": 0.0,
                "visits": 0,
                "last_seen": time.time()
            }

        node = nodes[node_id]

        # reinforcement learning update
        node["activation"] = node["activation"] * 0.95 + signal_strength * 0.05
        node["visits"] += 1
        node["last_seen"] = time.time()

        graph["nodes"] = nodes

        self._atomic_write(graph)

    # -------------------------
    # EDGE LEARNING (RELATIONSHIPS)
    # -------------------------
    def update_edge(self, a, b, weight=1.0):
        graph = self.read()
        edges = graph["edges"]

        key = f"{a}->{b}"

        if key not in edges:
            edges[key] = {
                "weight": 0.0,
                "count": 0
            }

        edge = edges[key]

        # reinforcement + decay hybrid
        edge["weight"] = edge["weight"] * 0.97 + weight * 0.03
        edge["count"] += 1

        graph["edges"] = edges

        self._atomic_write(graph)

    # -------------------------
    # CO-ACTIVATION LEARNING
    # -------------------------
    def reinforce_batch(self, active_nodes):
        """
        Strengthen connections between simultaneously active nodes
        """
        for i in range(len(active_nodes)):
            for j in range(i + 1, len(active_nodes)):
                self.update_edge(active_nodes[i], active_nodes[j], weight=1.0)

    # -------------------------
    # QUERY GRAPH STATE
    # -------------------------
    def get_state(self):
        return self.read()
