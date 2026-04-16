import time
import threading

class SwarmRegistry:
    def __init__(self):
        self.nodes = {}
        self.lock = threading.Lock()

    def register_peer(self, node_id, ip, meta=None):
        with self.lock:
            if node_id not in self.nodes:
                self.nodes[node_id] = {
                    "ip": ip,
                    "trusted": False,
                    "meta": meta or {},
                    "last_seen": time.time()
                }
            else:
                self.nodes[node_id]["last_seen"] = time.time()

    def mark_trusted(self, node_id):
        with self.lock:
            if node_id in self.nodes:
                self.nodes[node_id]["trusted"] = True

    def get_trusted_nodes(self):
        with self.lock:
            return {
                k: v for k, v in self.nodes.items()
                if v["trusted"]
            }

    def get_all_nodes(self):
        with self.lock:
            return self.nodes
