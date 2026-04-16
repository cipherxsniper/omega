import time

class NodeRegistryV75:
    def __init__(self, ttl=20):
        self.peers = {}
        self.ttl = ttl

    def update(self, node_id):
        self.peers[node_id] = time.time()

    def prune(self):
        now = time.time()
        self.peers = {
            k: v for k, v in self.peers.items()
            if now - v < self.ttl
        }

    def count(self):
        self.prune()
        return len(self.peers)
