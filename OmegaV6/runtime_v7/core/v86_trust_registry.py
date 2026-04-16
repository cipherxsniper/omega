import time


class TrustRegistryV86:
    def __init__(self):
        self.peers = {}

    def register(self, node_id):
        self.peers[node_id] = {
            "trust": 1.0,
            "last_seen": time.time(),
            "status": "active"
        }

    def is_trusted(self, node_id):
        peer = self.peers.get(node_id)

        if not peer:
            return False

        # expire stale nodes
        if time.time() - peer["last_seen"] > 60:
            return False

        return peer["trust"] > 0.3

    def update_seen(self, node_id):
        if node_id in self.peers:
            self.peers[node_id]["last_seen"] = time.time()
