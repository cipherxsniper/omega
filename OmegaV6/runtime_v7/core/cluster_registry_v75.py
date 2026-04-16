import time

class ClusterRegistryV75:
    def __init__(self, ttl=30):
        self.peers = {}
        self.ttl = ttl

    def register(self, node_id, sig):
        self.peers[node_id] = {
            "sig": sig,
            "last_seen": time.time()
        }

    def verify(self, node_id, sig):
        peer = self.peers.get(node_id)
        return peer is not None and peer["sig"] == sig

    def heartbeat(self, node_id):
        if node_id in self.peers:
            self.peers[node_id]["last_seen"] = time.time()

    def prune(self):
        now = time.time()
        self.peers = {
            k: v for k, v in self.peers.items()
            if now - v["last_seen"] < self.ttl
        }

    def snapshot(self):
        self.prune()
        return self.peers
