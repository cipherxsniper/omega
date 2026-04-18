import time

class NodeRegistry:

    def __init__(self):
        self.nodes = {}

    def register(self, node_id):

        self.nodes[node_id] = {
            "status": "alive",
            "last_seen": time.time()
        }

    def heartbeat(self, node_id):

        if node_id in self.nodes:
            self.nodes[node_id]["last_seen"] = time.time()
            self.nodes[node_id]["status"] = "alive"

    def cleanup(self, timeout=10):

        now = time.time()

        for node in self.nodes:

            if now - self.nodes[node]["last_seen"] > timeout:
                self.nodes[node]["status"] = "dead"

    def active_nodes(self):

        return [n for n, d in self.nodes.items() if d["status"] == "alive"]
