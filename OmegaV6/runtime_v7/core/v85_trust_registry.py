import time

class TrustRegistryV85:
    def __init__(self):
        self.peers = {}

    def validate_peer(self, node_id, trust_score=1.0):
        self.peers[node_id] = {
            "trust": trust_score,
            "last_seen": time.time()
        }

    def is_trusted(self, node_id):
        peer = self.peers.get(node_id)
        if not peer:
            return False

        # expire stale nodes
        if time.time() - peer["last_seen"] > 30:
            return False

        return peer["trust"] > 0.5

    def cleanup(self):
        now = time.time()
        self.peers = {
            k: v for k, v in self.peers.items()
            if now - v["last_seen"] <= 30
        }
